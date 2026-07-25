def test_create_category(client, auth_headers):
    response = client.post("/api/v1/categorias", headers=auth_headers, json={"name": "Alimentação"})
    assert response.status_code == 201
    assert response.json()["name"] == "Alimentação"


def test_list_categories(client, auth_headers):
    client.post("/api/v1/categorias", headers=auth_headers, json={"name": "Transporte"})
    client.post("/api/v1/categorias", headers=auth_headers, json={"name": "Moradia"})

    response = client.get("/api/v1/categorias", headers=auth_headers)
    assert response.status_code == 200
    names = [c["name"] for c in response.json()]
    assert "Transporte" in names
    assert "Moradia" in names


def test_update_category(client, auth_headers):
    create = client.post("/api/v1/categorias", headers=auth_headers, json={"name": "Lazer"})
    cat_id = create.json()["id"]

    response = client.put(f"/api/v1/categorias/{cat_id}", headers=auth_headers, json={"name": "Entretenimento"})
    assert response.status_code == 200
    assert response.json()["name"] == "Entretenimento"


def test_update_nonexistent_category_returns_404(client, auth_headers):
    response = client.put(
        "/api/v1/categorias/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
        json={"name": "X"},
    )
    assert response.status_code == 404


def test_delete_category(client, auth_headers):
    create = client.post("/api/v1/categorias", headers=auth_headers, json={"name": "Temporária"})
    cat_id = create.json()["id"]

    delete_response = client.delete(f"/api/v1/categorias/{cat_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    remaining = client.get("/api/v1/categorias", headers=auth_headers).json()
    assert all(c["id"] != cat_id for c in remaining)


def test_expense_category_becomes_null_after_category_deleted(client, auth_headers):
    """Ao excluir uma categoria, gastos vinculados viram 'sem categoria' (SET NULL)."""
    cat = client.post("/api/v1/categorias", headers=auth_headers, json={"name": "Para deletar"}).json()
    expense = client.post(
        "/api/v1/gastos",
        headers=auth_headers,
        json={"description": "Gasto vinculado", "amount": "50.00", "expense_date": "2026-07-01", "category_id": cat["id"]},
    ).json()

    client.delete(f"/api/v1/categorias/{cat['id']}", headers=auth_headers)

    updated = client.get(f"/api/v1/gastos/{expense['id']}", headers=auth_headers).json()
    assert updated["category"] is None
