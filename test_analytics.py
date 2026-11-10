import sqlite3
from datetime import date
from backend.analytics import percent_change, low_stock


def test_percent_change_zero_baseline():
    assert percent_change(10, 0) == 100
    assert percent_change(0, 0) == 0


def test_low_stock_stockout_is_flagged():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript("""CREATE TABLE products(id INTEGER PRIMARY KEY,name TEXT,unit TEXT,stock REAL,pack_size REAL,price REAL,reorder_enabled INTEGER);
    CREATE TABLE sales(product_id INTEGER,qty REAL,price REAL,sold_at TEXT);""")
    db.execute("INSERT INTO products VALUES(1,'Atta','kg',0,5,50,1)")
    db.execute("INSERT INTO sales VALUES(1,7,50,'2025-01-01')")
    assert low_stock(db, date(2025, 1, 8))[0]["days_of_stock_left"] == 0


def test_low_stock_ignores_new_item_with_stock():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript("""CREATE TABLE products(id INTEGER PRIMARY KEY,name TEXT,unit TEXT,stock REAL,pack_size REAL,price REAL,reorder_enabled INTEGER);
    CREATE TABLE sales(product_id INTEGER,qty REAL,price REAL,sold_at TEXT);""")
    db.execute("INSERT INTO products VALUES(1,'New','piece',10,1,5,1)")
    assert low_stock(db, date(2025, 1, 8)) == []

