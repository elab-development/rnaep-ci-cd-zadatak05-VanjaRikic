def test_order_can_be_saved_and_loaded_from_redis():
    import main

    order = main.Order(
        product_id="integration-product-1",
        price=50,
        fee=10,
        total=120,
        quantity=2,
        status="pending"
    )

    order.save()

    loaded_order = main.Order.get(order.pk)

    assert loaded_order.product_id == "integration-product-1"
    assert loaded_order.price == 50
    assert loaded_order.fee == 10
    assert loaded_order.total == 120
    assert loaded_order.quantity == 2
    assert loaded_order.status == "pending"


def test_order_completed_event_is_written_to_redis_stream():
    import main

    order = main.Order(
        product_id="stream-product-1",
        price=30,
        fee=6,
        total=36,
        quantity=1,
        status="completed"
    )

    event_id = main.redis.xadd("order_completed", order.model_dump(), "*")

    assert event_id is not None

    events = main.redis.xread({"order_completed": "0-0"}, count=1)

    assert len(events) > 0