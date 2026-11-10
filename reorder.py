import math
from typing import Any
from .db import connect


def suggested_quantity(avg_daily_sales: float, current_stock: float, lead_days: float, safety_factor: float, pack_size: float) -> float:
    target = max(0, avg_daily_sales * lead_days * safety_factor - current_stock)
    return math.ceil(target / pack_size) * pack_size if target else 0


def build_order(summary: dict[str, Any], lead_days: float = 3, safety_factor: float = 1.5) -> list[dict[str, Any]]:
    with connect() as db:
        order = []
        for item in summary.get("low_stock", []):
            p = db.execute("SELECT pack_size, price FROM products WHERE name=?", (item["item"],)).fetchone()
            if p:
                qty = suggested_quantity(item["avg_daily_sales"], item["stock"], lead_days, safety_factor, p["pack_size"])
                if qty:
                    order.append({**item, "order_qty": qty, "pack_size": p["pack_size"], "estimated_cost": round(qty * p["price"], 2)})
        return order

