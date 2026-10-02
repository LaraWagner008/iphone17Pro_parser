import sqlite3
from datetime import datetime

DB_NAME = "prices.db"

def init_db():
    """Создаёт таблицу, если её ещё нет."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iphone17_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store TEXT NOT NULL,
                price INTEGER NOT NULL,
                parsed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_price(store: str, price: int):
    """Сохраняет цену магазина в базу."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO iphone17_prices (store, price) VALUES (?, ?)",
            (store, price)
        )
        conn.commit()
    print(f"[DB] {store}: {price} руб. сохранено в базу.")

def get_price_history(store: str):
    """Возвращает историю цен для магазина (для будущей динамики)."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT price, parsed_at FROM iphone17_prices WHERE store = ? ORDER BY parsed_at DESC",
            (store,)
        )
        return cursor.fetchall()