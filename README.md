# Task Manager & JWT Auth API

RESTful API built with **Python**, **FastAPI**, **SQLAlchemy**, and **JWT (JSON Web Tokens)** featuring secure password hashing, user authentication, and user-isolated task CRUD operations.

## Tech Stack

- **Python 3.11+**
- **FastAPI** (Web framework & interactive OpenAPI/Swagger UI)
- **SQLAlchemy & SQLite** (Relational ORM with 1:N User-to-Tasks relationship)
- **PyJWT & Pwdlib (Bcrypt)** (JWT Bearer token generation and password hashing)
- **Pydantic** (Request validation and response serialization)
- **Pytest & HTTPX** (Automated integration and security tests)

## API Endpoints

### Authentication (Public)
- `POST /register` — Registers a new user with hashed password (`201 Created`).
- `POST /login` — Authenticates credentials and returns a JWT `access_token` (`200 OK`).

### Tasks (Protected — Requires `Bearer <token>`)
- `POST /tasks` — Creates a new task linked to the authenticated user (`201 Created`).
- `GET /tasks` — Lists all tasks belonging to the authenticated user (`200 OK`).
- `PATCH /tasks/{task_id}` — Updates task title, description, or completion status (`200 OK`).
- `DELETE /tasks/{task_id}` — Deletes a task owned by the authenticated user (`204 No Content`).

## Running Locally

```bash
git clone https://github.com
cd task-manager-auth-api

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Interactive Swagger documentation: `http://localhost:8000/docs`

## Running Automated Tests

```bash
pytest
```
