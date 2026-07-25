def test_register_new_user(client):
    response = client.post(
        "/api/v1/auth/register", json={"email": "novo@example.com", "password": "senha12345"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "novo@example.com"
    assert "hashed_password" not in body  # nunca deve vazar o hash


def test_register_duplicate_email_fails(client):
    client.post("/api/v1/auth/register", json={"email": "dup@example.com", "password": "senha12345"})
    response = client.post("/api/v1/auth/register", json={"email": "dup@example.com", "password": "outrasenha"})
    assert response.status_code == 409


def test_login_success_returns_token(client):
    client.post("/api/v1/auth/register", json={"email": "login@example.com", "password": "senha12345"})
    response = client.post(
        "/api/v1/auth/login", json={"email": "login@example.com", "password": "senha12345"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert len(response.json()["access_token"]) > 10


def test_login_wrong_password_fails(client):
    client.post("/api/v1/auth/register", json={"email": "wrong@example.com", "password": "senha12345"})
    response = client.post(
        "/api/v1/auth/login", json={"email": "wrong@example.com", "password": "errada123"}
    )
    assert response.status_code == 401


def test_access_protected_route_without_token_fails(client):
    response = client.get("/api/v1/gastos")
    assert response.status_code == 401
