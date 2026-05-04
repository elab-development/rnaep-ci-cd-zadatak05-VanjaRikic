import pytest


class FakeResponse:
    status_code = 200

    def json(self):
        return {
            "id": "product-1",
            "name": "Test Product",
            "price": 100,
            "quantity": 10
        }


class FakeAsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def get(self, url):
        return FakeResponse()


@pytest.mark.asyncio
async def test_create_order_business_logic(monkeypatch):
    import main

    saved_orders = []

    def fake_save(self):
        saved_orders.append(self)
        return self

    async def fake_process_order(order):
        order.status = "completed"

    monkeypatch.setattr(main.httpx, "AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(main.Order, "save", fake_save)
    monkeypatch.setattr(main, "process_order", fake_process_order)

    class FakeBackgroundTasks:
        def add_task(self, task, order):
            pass

    response = await main.create_order(
        body={
            "id": "product-1",
            "quantity": 2
        },
        background_tasks=FakeBackgroundTasks()
    )

    assert response.product_id == "product-1"
    assert response.price == 100
    assert response.fee == 20
    assert response.total == 240
    assert response.quantity == 2
    assert response.status == "pending"
    assert len(saved_orders) == 1