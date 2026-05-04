from fastapi.testclient import TestClient


class FakeResponse:
    status_code = 200

    def json(self):
        return {
            "id": "product-functional-1",
            "name": "Functional Product",
            "price": 200,
            "quantity": 5
        }


class FakeAsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, url):
        return FakeResponse()


def test_create_order_api_flow(monkeypatch):
    import main

    async def fake_process_order(order):
        order.status = "completed"

    monkeypatch.setattr(main.httpx, "AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(main, "process_order", fake_process_order)

    client = TestClient(main.app)

    response = client.post(
        "/orders",
        json={
            "id": "product-functional-1",
            "quantity": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == "product-functional-1"
    assert data["price"] == 200
    assert data["fee"] == 40
    assert data["total"] == 480
    assert data["quantity"] == 2
    assert data["status"] == "pending"


def test_get_non_existing_order_returns_404():
    import main

    client = TestClient(main.app)

    response = client.get("/orders/non-existing-order-id")

    assert response.status_code == 404