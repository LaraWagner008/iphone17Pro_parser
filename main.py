from db_utils import init_db, save_price, get_price_history
from parsers import parse_re_store, parse_mvideo, parse_05ru, parse_real2, parse_citilink

def run_parsing():
    print("🚀 Запуск парсинга iPhone 17 Pro 512GB White...")
    init_db()
    
    stores = {
        "re-store": parse_re_store,
        "mvideo": parse_mvideo,
        #"dns": parse_dns,
        "05.ru": parse_05ru,
        "real2": parse_real2,
        "citilink": parse_citilink,
    }

    for store_name, parser_func in stores.items():
        price = parser_func()
        if price:
            save_price(store_name, price)
        else:
            print(f"⚠️ {store_name}: цену найти не удалось (возможно, сайт защищён или селектор устарел)")
    
    print("\n📊 История цен (последние 5 записей по каждому магазину):")
    for store_name in stores:
        history = get_price_history(store_name)
        print(f"\n--- {store_name} ---")
        for price, date in history[:5]:
            print(f"  {date}: {price} руб.")

if __name__ == "__main__":
    run_parsing()