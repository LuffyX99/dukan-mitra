import re
from typing import Any

NUMBERS = {"ek": 1, "one": 1, "do": 2, "do": 2, "teen": 3, "tin": 3, "char": 4, "paanch": 5, "bees": 20, "dus": 10}
REGIONAL_SALES = {"மூன்று": 3, "மூன்று": 3, "तीन": 3}


def _number(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return NUMBERS.get(value.lower())


def extract_intent(text: str) -> dict[str, Any]:
    t = text.lower().strip()
    regional = re.search(r"(மூன்று|तीन)\s+([^\s]+)", t)
    if regional and any(word in t for word in ("விற்ற", "बिकी", "बिका")):
        return {"intent": "log_sale", "entities": [{"qty": REGIONAL_SALES[regional.group(1)], "item": regional.group(2), "type": "cash"}]}
    if any(x in t for x in ("repeat", "phir se", "dobara")): return {"intent": "repeat", "entities": {}}
    if "slower" in t or "dheere" in t: return {"intent": "slower", "entities": {}}
    if "skip" in t or "chhod" in t: return {"intent": "skip", "entities": {}}
    if "order mat" in t or "don't order" in t: return {"intent": "reject_order", "entities": {}}
    if "order" in t or "mangwa" in t or "approve" in t: return {"intent": "approve_order", "entities": {}}
    match = re.search(r"([a-z][a-z0-9]*)\s+(?:kitna|kitne|bacha|stock)", t)
    if match and not any(x in t for x in ("bika", "diye")): return {"intent": "stock_query", "entities": {"item": match.group(1).strip()}}
    corrections = re.search(r"([a-z][a-z ]{1,20})\s+(\d+(?:\.\d+)?)\s*(?:kar do|kardo)", t)
    if corrections: return {"intent": "correct_order", "entities": {"item": corrections.group(1).strip(), "qty": float(corrections.group(2))}}
    matches = re.findall(r"(\d+(?:\.\d+)?|ek|do|teen|tin|char|paanch|bees|dus)\s+(?:kilo|kg|packet|pack|pcs|piece)?\s*([a-z][a-z0-9 ]*?)(?=\s+(?:aur|bika|biki|diye|udhaar|aaj|$))", t)
    if matches:
        entities = [{"qty": _number(qty), "item": item.strip(), "type": "credit" if "udhaar" in t else "cash"} for qty, item in matches]
        return {"intent": "log_sale", "entities": entities}
    return {"intent": "unknown", "entities": {}}
