from datetime import date, timedelta
from typing import Any
from .db import connect


def _sales_total(db, start: date, end: date) -> float:
    row = db.execute(
        "SELECT COALESCE(SUM(qty * price), 0) total FROM sales WHERE date(sold_at) >= ? AND date(sold_at) <= ?",
        (start.isoformat(), end.isoformat()),
    ).fetchone()
    return float(row["total"])


def percent_change(current: float, previous: float) -> float:
    return round((current - previous) / previous * 100, 1) if previous else (100.0 if current else 0.0)


def sales_comparison(db, day: date) -> dict[str, float]:
    today = _sales_total(db, day, day)
    yesterday = _sales_total(db, day - timedelta(days=1), day - timedelta(days=1))
    weekday = day - timedelta(days=7)
    last_week = _sales_total(db, weekday, weekday)
    return {
        "total_sales_today": round(today, 2),
        "vs_yesterday_pct": percent_change(today, yesterday),
        "vs_same_weekday_last_week_pct": percent_change(today, last_week),
    }


def ranked_items(db, day: date, limit: int = 3) -> dict[str, list[dict[str, Any]]]:
    rowset = db.execute(
        """SELECT p.name, p.unit, SUM(s.qty) qty, SUM(s.qty*s.price) revenue
           FROM sales s JOIN products p ON p.id=s.product_id
           WHERE date(s.sold_at)=? GROUP BY p.id ORDER BY qty DESC""",
        (day.isoformat(),),
    ).fetchall()
    items = [{"item": r["name"], "unit": r["unit"], "qty": round(r["qty"], 2), "revenue": round(r["revenue"], 2)} for r in rowset]
    return {"by_quantity": items[:limit], "by_revenue": sorted(items, key=lambda x: x["revenue"], reverse=True)[:limit]}


def low_stock(db, day: date, threshold_days: float = 2, lookback: int = 7) -> list[dict[str, Any]]:
    products = db.execute("SELECT * FROM products WHERE reorder_enabled=1").fetchall()
    result = []
    start = day - timedelta(days=lookback)
    for p in products:
        avg = db.execute(
            "SELECT COALESCE(SUM(qty),0)/? avg_qty FROM sales WHERE product_id=? AND date(sold_at)>? AND date(sold_at)<=?",
            (lookback, p["id"], start.isoformat(), day.isoformat()),
        ).fetchone()["avg_qty"]
        days = (p["stock"] / avg) if avg else (float("inf") if p["stock"] > 0 else 0)
        if days < threshold_days:
            result.append({"item": p["name"], "stock": p["stock"], "unit": p["unit"], "avg_daily_sales": round(avg, 2), "days_of_stock_left": round(days, 2) if avg else 0})
    return sorted(result, key=lambda x: x["days_of_stock_left"])


def slow_movers(db, day: date) -> list[str]:
    start = day - timedelta(days=7)
    return [r["name"] for r in db.execute(
        """SELECT p.name FROM products p LEFT JOIN sales s ON p.id=s.product_id AND date(s.sold_at)>? AND date(s.sold_at)<=?
           GROUP BY p.id HAVING COALESCE(SUM(s.qty),0)=0""", (start.isoformat(), day.isoformat())).fetchall()]


def udhaar_summary(db) -> dict[str, Any]:
    rows = db.execute("""SELECT COALESCE(customer,'Unknown') customer, SUM(qty*price) amount
        FROM sales WHERE sale_type='credit' GROUP BY customer ORDER BY amount DESC""").fetchall()
    return {"total_pending_credit": round(sum(r["amount"] for r in rows), 2),
            "top_debtors": [{"customer": r["customer"], "amount": round(r["amount"], 2)} for r in rows[:3]]}


def daily_summary(day: date | None = None, threshold_days: float = 2) -> dict[str, Any]:
    day = day or date.today()
    with connect() as db:
        return {**sales_comparison(db, day), "top_sellers": ranked_items(db, day),
                "low_stock": low_stock(db, day, threshold_days), "slow_movers": slow_movers(db, day),
                "udhaar": udhaar_summary(db)}

