from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_and_read_work_order():
    create_response = client.post(
        "/work-orders",
        json={
            "title": "Test work order",
            "status": "open",
        },
    )

    assert create_response.status_code == 200

    created = create_response.json()

    assert created["title"] == "Test work order"
    assert created["status"] == "open"
    assert "id" in created

    work_order_id = created["id"]

    read_response = client.get(f"/work-orders/{work_order_id}")

    assert read_response.status_code == 200

    fetched = read_response.json()

    assert fetched["id"] == work_order_id
    assert fetched["title"] == "Test work order"
    assert fetched["status"] == "open"

def test_invalid_work_order_returns_400():
    response = client.post(
        "/work-orders",
        json={"title": "Missing status"},
    )

    assert response.status_code == 400

def test_unknown_work_order_returns_404():
    response = client.get("/work-orders/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Work order not found"
