from datetime import date, timedelta
import random
from .db import connect, init_db

PRODUCTS = [("Atta", "kg", 20, 5, 48), ("Maggi", "packet", 30, 10, 14), ("Doodh", "packet", 12, 6, 28), ("Chawal", "kg", 25, 5, 62), ("Tel", "litre", 18, 1, 125), ("Biscuit", "packet", 40, 10, 10), ("Chai", "packet", 15, 2, 220), ("Cheeni", "kg", 20, 5, 45)]


def seed(days: int = 30) -> None:
    init_db()
    random.seed(7)
    with connect() as db:
        for name, unit, stock, pack, price in PRODUCTS:
            db.execute("INSERT OR IGNORE INTO products(name,unit,stock,pack_size,price) VALUES(?,?,?,?,?)", (name, unit, stock, pack, price))
        ids = {r["name"]: r["id"] for r in db.execute("SELECT id,name FROM products")}
        for offset in range(days, 0, -1):
            day = date.today() - timedelta(days=offset)
            for name, _, _, _, price in PRODUCTS:
                qty = random.randint(1, 8) * (2 if day.weekday() >= 5 else 1)
                if offset in (10, 20): qty *= 2
                db.execute("INSERT INTO sales(product_id,qty,price,sold_at) VALUES(?,?,?,?)", (ids[name], qty, price, day.isoformat()))
                db.execute("UPDATE products SET stock=stock-? WHERE id=?", (qty, ids[name]))
        db.commit()


if __name__ == "__main__":
    seed()
