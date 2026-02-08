# Quickstart Guide: Backend Integration

**Feature**: Full Backend + Frontend Integration
**Branch**: `1-backend-integration`
**Date**: 2026-02-07

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL account (https://neon.tech)
- Git
- Code editor (VS Code recommended)

## Step 1: Environment Setup

### 1.1 Clone Repository (if needed)

```bash
git clone <repository-url>
cd <repository-name>
git checkout 1-backend-integration
```

### 1.2 Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 1.3 Install Dependencies

```bash
# Using pip
cd backend
pip install fastapi sqlmodel pyjwt psycopg2-binary python-dotenv uvicorn

# Or using uv (recommended)
uv pip install fastapi sqlmodel pyjwt psycopg2-binary python-dotenv uvicorn
```

## Step 2: Configuration

### 2.1 Get Neon Database URL

1. Go to https://neon.tech
2. Create a new project (if needed)
3. Copy the connection string (format: `postgresql://user:pass@host/dbname`)

### 2.2 Get BETTER_AUTH_SECRET

Coordinate with frontend team to obtain the shared `BETTER_AUTH_SECRET` used by Better Auth.

**CRITICAL**: Frontend and backend MUST use the same secret!

### 2.3 Create .env File

Create `backend/.env` file (NEVER commit this file):

```env
# Database
DATABASE_URL=postgresql://user:password@ep-example.us-east-2.aws.neon.tech/neondb

# Authentication (MUST match frontend)
BETTER_AUTH_SECRET=your-shared-secret-here-min-32-chars

# CORS (Frontend URL)
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

### 2.4 Verify .gitignore

Ensure `.gitignore` includes:

```
.env
.env.*
!.env.example
__pycache__/
*.pyc
.pytest_cache/
```

## Step 3: Database Initialization

### 3.1 Run Database Migrations

```bash
cd backend

# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create tasks table"

# Apply migration
alembic upgrade head
```

### 3.2 Verify Database

```bash
# Test database connection
python -c "
from db import engine
from sqlmodel import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connection successful!')
"
```

## Step 4: Run Development Server

### 4.1 Start FastAPI Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4.2 Verify Server Running

Open browser to http://localhost:8000/docs

You should see the auto-generated Swagger UI.

## Step 5: Testing with curl

### 5.1 Get JWT Token

**Option A**: Use frontend to login and copy JWT from browser DevTools (Application > Local Storage)

**Option B**: Generate test token (development only):

```python
# test_token.py
import jwt
from datetime import datetime, timedelta

secret = "your-shared-secret"
payload = {
    "sub": "test-user-123",
    "exp": datetime.utcnow() + timedelta(hours=1),
    "iat": datetime.utcnow()
}
token = jwt.encode(payload, secret, algorithm="HS256")
print(f"Bearer {token}")
```

### 5.2 Test Endpoints

```bash
# Store token in variable
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# List tasks (empty initially)
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tasks

# Create task
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","description":"Milk, eggs, bread"}' \
  http://localhost:8000/api/tasks

# Get task by ID
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tasks/1

# Update task
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries and snacks","completed":true}' \
  http://localhost:8000/api/tasks/1

# Toggle completion
curl -X PATCH -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tasks/1/complete

# Delete task
curl -X DELETE -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/tasks/1
```

## Step 6: Frontend Integration

### 6.1 Start Frontend

```bash
# In separate terminal
cd frontend
npm install  # if needed
npm run dev
```

Frontend should run on http://localhost:3000

### 6.2 Configure Frontend API URL

Update frontend environment variables (e.g., `.env.local`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 6.3 Test Full Flow

1. Open http://localhost:3000
2. Login via Better Auth
3. Create a task
4. See task appear in list
5. Toggle completion
6. Delete task

## Step 7: Running Tests

### 7.1 Install Test Dependencies

```bash
cd backend
pip install pytest pytest-asyncio httpx
```

### 7.2 Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Ensure virtual environment is activated and dependencies are installed

```bash
source venv/bin/activate  # or .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Database connection fails

**Solution**: Verify DATABASE_URL in .env

```bash
# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### Issue: 401 Unauthorized on all requests

**Solution**: Verify BETTER_AUTH_SECRET matches frontend

1. Check frontend .env for BETTER_AUTH_SECRET
2. Ensure backend .env has same value
3. Restart both servers

### Issue: CORS errors in browser

**Solution**: Verify FRONTEND_URL in backend .env

```bash
# backend/.env
FRONTEND_URL=http://localhost:3000
```

Restart backend server after changing .env

### Issue: Frontend can't connect to backend

**Solution**: Verify backend is running and frontend API URL is correct

```bash
# Test backend health
curl http://localhost:8000/docs

# Check frontend env
cat frontend/.env.local | grep API_URL
```

## Development Workflow

### Making Changes

1. Make code changes
2. Backend auto-reloads (if `--reload` flag used)
3. Test changes with curl or frontend
4. Write/update tests
5. Run tests: `pytest`
6. Commit changes

### Adding New Endpoints

1. Define endpoint in `routes/tasks.py` (or new router)
2. Update OpenAPI spec in `contracts/openapi.yaml`
3. Add tests in `tests/`
4. Update this quickstart guide if needed

### Database Changes

1. Modify SQLModel models in `models.py`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration in `alembic/versions/`
4. Apply migration: `alembic upgrade head`
5. Update `data-model.md` documentation

## Next Steps

- Review `specs/1-backend-integration/plan.md` for implementation phases
- Check `specs/1-backend-integration/research.md` for architectural decisions
- See `specs/1-backend-integration/data-model.md` for database schema
- Explore `specs/1-backend-integration/contracts/openapi.yaml` for API contract

## Useful Commands

```bash
# Backend
uvicorn main:app --reload                    # Start dev server
pytest                                       # Run tests
alembic upgrade head                         # Apply migrations
alembic revision --autogenerate -m "msg"     # Create migration

# Frontend
npm run dev                                  # Start Next.js dev server
npm run build                                # Build for production
npm test                                     # Run frontend tests

# Database
psql $DATABASE_URL                           # Connect to database
alembic current                              # Show current migration
alembic downgrade -1                         # Rollback one migration
```

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLModel Docs: https://sqlmodel.tiangolo.com/
- Neon Docs: https://neon.tech/docs
- Better Auth: https://www.better-auth.com/docs
- PyJWT: https://pyjwt.readthedocs.io/

---

**Happy Coding!** 🚀

For issues or questions, refer to the planning documents in `specs/1-backend-integration/` or contact the team.
