import json
import os
from datetime import datetime
from parsers import parse_re_store, parse_mvideo, parse_05ru, parse_real2, parse_citilink

DATA_FILE = "data/prices.json"


def load_prices():
    """Загружает текущие цены из JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_prices(data):
    """Сохраняет цены в JSON."""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_parsing():
    print("🚀 Запуск парсинга iPhone 17 Pro 512GB White...")
    data = load_prices()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    stores = {
        "re-store": parse_re_store,
        "mvideo": parse_mvideo,
        "05.ru": parse_05ru,
        "real2": parse_real2,
        "citilink": parse_citilink,
    }

    for store_name, parser_func in stores.items():
        price = parser_func()
        if price:
            if store_name not in data:
                data[store_name] = []
            data[store_name].append({
                "price": price,
                "date": timestamp
            })
            print(f"[JSON] {store_name}: {price} руб. сохранено")
        else:
            print(f"⚠️ {store_name}: цену найти не удалось")

    save_prices(data)
    print("\n📊 Данные сохранены в data/prices.json")


if __name__ == "__main__":
    run_parsing()