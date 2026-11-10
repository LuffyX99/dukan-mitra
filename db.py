import os
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("DATABASE_PATH", "dukaan_mitra.db"))


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, unit TEXT NOT NULL,
                stock REAL NOT NULL DEFAULT 0, pack_size REAL NOT NULL DEFAULT 1,
                price REAL NOT NULL DEFAULT 0, reorder_enabled INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL, qty REAL NOT NULL,
                price REAL NOT NULL, customer TEXT, sale_type TEXT NOT NULL DEFAULT 'cash',
                sold_at TEXT NOT NULL, FOREIGN KEY(product_id) REFERENCES products(id)
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY, status TEXT NOT NULL, created_at TEXT NOT NULL,
                payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY, metric TEXT NOT NULL, value REAL NOT NULL,
                recorded_at TEXT NOT NULL
            );
            """
        )


def rows(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with connect() as db:
        return [dict(row) for row in db.execute(sql, params).fetchall()]
