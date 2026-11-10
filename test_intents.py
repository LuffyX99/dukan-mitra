from backend.intents import extract_intent


def test_hinglish_multi_sale():
    result = extract_intent("do kilo atta aur teen Maggi bika aaj")
    assert result["intent"] == "log_sale"
    assert [(x["qty"], x["item"]) for x in result["entities"]] == [(2, "atta"), (3, "maggi")]


def test_hinglish_stock_query():
    assert extract_intent("Maggi kitna bacha?") == {"intent": "stock_query", "entities": {"item": "maggi"}}


def test_regional_code_mixed_sale():
    result = extract_intent("teen maggi biki")
    assert result["entities"][0]["qty"] == 3

