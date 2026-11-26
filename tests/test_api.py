import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_tasks.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def get_auth_headers(email: str = "dev@example.com", password: str = "strongpass123"):
    client.post("/register", json={"email": email, "password": password})
    login_res = client.post(
        "/login", data={"username": email, "password": password}
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_unauthorized_access_blocked():
    response = client.get("/tasks")
    assert response.status_code == 401


def test_full_task_crud_and_user_isolation():
    headers_user1 = get_auth_headers("user1@example.com", "password123")
    headers_user2 = get_auth_headers("user2@example.com", "password123")

    # 1. Usuário 1 cria uma tarefa
    create_res = client.post(
        "/tasks",
        json={"title": "Estudar FastAPI e JWT", "description": "Concluir API de portfólio"},
        headers=headers_user1,
    )
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    # 2. Usuário 2 não pode ver nem alterar a tarefa do Usuário 1
    list_user2 = client.get("/tasks", headers=headers_user2)
    assert list_user2.status_code == 200
    assert len(list_user2.json()) == 0

    patch_user2 = client.patch(
        f"/tasks/{task_id}", json={"completed": True}, headers=headers_user2
    )
    assert patch_user2.status_code == 404

    # 3. Usuário 1 marca a tarefa como concluída e depois exclui
    patch_user1 = client.patch(
        f"/tasks/{task_id}", json={"completed": True}, headers=headers_user1
    )
    assert patch_user1.status_code == 200
    assert patch_user1.json()["completed"] is True

    delete_user1 = client.delete(f"/tasks/{task_id}", headers=headers_user1)
    assert delete_user1.status_code == 204
