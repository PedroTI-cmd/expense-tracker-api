def test_create_expense(client, auth_headers):
    response = client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Almoço", "amount": "35.50", "expense_date": "2026-07-20"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["description"] == "Almoço"
    assert body["amount"] == "35.50"


def test_create_expense_with_invalid_category_fails(client, auth_headers):
    response = client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={
            "description": "Mercado",
            "amount": "100.00",
            "expense_date": "2026-07-20",
            "category_id": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert response.status_code == 404


def test_list_expenses_only_returns_own_expenses(client, auth_headers):
    client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Gasto do usuário 1", "amount": "10.00", "expense_date": "2026-07-01"},
    )

    # segundo usuário não deve ver o gasto do primeiro
    client.post("/api/v1/auth/register", json={"email": "outro@example.com", "password": "senha12345"})
    login = client.post("/api/v1/auth/login", json={"email": "outro@example.com", "password": "senha12345"})
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.get("/api/v1/gastos", headers=other_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_update_expense(client, auth_headers):
    create = client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Original", "amount": "50.00", "expense_date": "2026-07-01"},
    )
    expense_id = create.json()["id"]

    response = client.patch(
        f"/api/v1/gastos/{expense_id}", headers=auth_headers, json={"description": "Atualizado"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Atualizado"


def test_delete_expense(client, auth_headers):
    create = client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Para deletar", "amount": "20.00", "expense_date": "2026-07-01"},
    )
    expense_id = create.json()["id"]

    delete_response = client.delete(f"/api/v1/gastos/{expense_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/gastos/{expense_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_monthly_summary(client, auth_headers):
    client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Gasto 1", "amount": "30.00", "expense_date": "2026-07-05"},
    )
    client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Gasto 2", "amount": "20.00", "expense_date": "2026-07-15"},
    )

    response = client.get("/api/v1/gastos/resumo-mensal?year=2026&month=7", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total"] == "50.00"
