# Task Management API - Backend

FastAPI backend for secure task management with JWT authentication and PostgreSQL database.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL account (https://neon.tech)
- Git

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start development server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── db.py                # Database engine and session management
├── models.py            # SQLModel database models
├── auth.py              # JWT authentication logic
├── schemas.py           # Pydantic request/response schemas
├── routes/
│   ├── __init__.py
│   └── tasks.py         # Task CRUD endpoints
├── core/
│   ├── __init__.py
│   └── config.py        # Environment configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Pytest fixtures
│   ├── test_auth.py     # Authentication tests
│   ├── test_tasks.py    # Task endpoint tests
│   └── test_isolation.py # Data isolation tests
├── alembic/             # Database migrations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## Environment Variables

Required variables in `.env`:

- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared secret with frontend (min 32 chars)
- `FRONTEND_URL`: Frontend URL for CORS (e.g., http://localhost:3000)
- `ENVIRONMENT`: deployment environment (development/staging/production)

## API Endpoints

All endpoints require `Authorization: Bearer <jwt_token>` header.

### Tasks

- `GET /api/tasks` - List user's tasks (optional ?status=completed|active)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Development

### Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

### Code Quality

Format code:
```bash
ruff format .
```

Lint code:
```bash
ruff check .
```

## Troubleshooting

### Database Connection Errors

- Verify `DATABASE_URL` in `.env` is correct
- Ensure Neon database is accessible
- Check connection pooling settings in `db.py`

### Authentication Errors (401)

- Verify `BETTER_AUTH_SECRET` matches frontend
- Check JWT token format (must include `sub` claim)
- Ensure token hasn't expired

### CORS Errors

- Verify `FRONTEND_URL` in `.env` matches actual frontend URL
- Check CORS middleware configuration in `main.py`
- Restart backend server after .env changes

## Architecture

- **Framework**: FastAPI (async Python web framework)
- **ORM**: SQLModel (type-safe database access)
- **Database**: Neon PostgreSQL (serverless Postgres)
- **Authentication**: JWT with HS256 algorithm
- **Testing**: pytest with FastAPI TestClient

## Security

- All endpoints require JWT authentication
- User data isolated by `user_id` from JWT
- Secrets managed via environment variables
- Input validation with Pydantic schemas
- SQL injection prevention via ORM
- CORS configured for specific origins

## Documentation

For detailed specifications, see:
- `/specs/1-backend-integration/spec.md` - Feature requirements
- `/specs/1-backend-integration/plan.md` - Implementation plan
- `/specs/1-backend-integration/data-model.md` - Database schema
- `/specs/1-backend-integration/contracts/openapi.yaml` - API specification

## Support

For issues or questions, refer to the planning documents in `/specs/1-backend-integration/`.
