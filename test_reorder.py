from backend.reorder import suggested_quantity


def test_reorder_rounds_to_pack_size():
    assert suggested_quantity(4, 2, 3, 1.5, 5) == 20


def test_reorder_never_negative():
    assert suggested_quantity(1, 20, 3, 1.5, 1) == 0

