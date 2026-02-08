"""Create tasks table with indexes

Revision ID: 001
Revises:
Create Date: 2026-02-07 17:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create tasks table with proper indexes for user data isolation.

    Implements FR-005: Task model with all required fields and indexes.
    """
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=10000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for query performance
    # Single index on user_id for user-specific queries
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])

    # Single index on completed for status filtering
    op.create_index('ix_tasks_completed', 'tasks', ['completed'])

    # Composite index for efficient user + status filtering
    op.create_index('idx_task_user_completed', 'tasks', ['user_id', 'completed'])

    # Create trigger to auto-update updated_at timestamp
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    op.execute("""
        CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Drop tasks table and related objects."""
    op.execute("DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")

    op.drop_index('idx_task_user_completed', table_name='tasks')
    op.drop_index('ix_tasks_completed', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')

    op.drop_table('tasks')
