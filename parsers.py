import json
import re
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def parse_re_store() -> int | None:
    """Парсит цену в re-store, вытаскивая JSON из window.__INITIAL_STATE__."""
    url = "https://re-store.ru/catalog/10117PRO512SLVN/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Ищем <script> с window.__INITIAL_STATE__
        target_script = None
        for script in soup.find_all("script"):
            if script.string and "window.__INITIAL_STATE__" in script.string:
                target_script = script.string
                break

        if not target_script:
            print("[re-store] window.__INITIAL_STATE__ не найден")
            return None

        # 2. Вырезаем JSON-строку
        match = re.search(
            r"window\.__INITIAL_STATE__\s*=\s*JSON\.parse\(\s*'(.*?)'\s*\)",
            target_script,
            re.DOTALL,
        )
        if not match:
            print("[re-store] Не удалось вырезать JSON-строку")
            return None

        json_str = match.group(1).encode().decode("unicode_escape")
        data = json.loads(json_str)

        # 3. Забираем точную цену по известному пути
        special_price = data.get("prices", {}).get("special", {}).get("price")
        if special_price:
            return int(special_price)

        print("[re-store] prices.special.price не найден в JSON")
    except Exception as e:
        print(f"[re-store] Ошибка: {e}")
    return None


from playwright.sync_api import sync_playwright


def parse_mvideo() -> int | None:
    """Парсит цену в М.Видео через Playwright."""
    url = "https://www.mvideo.ru/products/400480669"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            # Ждём загрузки и появления цены
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_selector("span.prices-base", timeout=15000)
            text = page.locator("span.prices-base").first.inner_text()
            browser.close()

        price = int(re.sub(r"[^\d]", "", text))
        return price
    except Exception as e:
        print(f"[mvideo] Ошибка: {e}")
    return None


'''
начинается DNS
import undetected_chromedriver as uc

def get_qrator_cookie() -> str | None:
    """Получает cookie qrator_jsid через undetected-chromedriver."""
    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(options=options, headless=True)

        # Заходим на главную DNS
        driver.get("https://www.dns-shop.ru/")
        time.sleep(5)

        # Проверяем cookie
        for cookie in driver.get_cookies():
            if cookie["name"] == "qrator_jsid":
                driver.quit()
                return cookie["value"]

        # Fallback: страница товара
        driver.get("https://www.dns-shop.ru/product/043f7f7d8dd4d0a4/63-smartfon-apple-iphone-17-pro-512-gb-serebristyj/")
        time.sleep(5)

        cookies = driver.get_cookies()
        driver.quit()

        for cookie in cookies:
            if cookie["name"] == "qrator_jsid":
                return cookie["value"]

    except Exception as e:
        print(f"[DNS] Ошибка получения qrator_jsid: {e}")
    return None


def parse_dns() -> int | None:
    """Парсит цену в DNS с использованием qrator_jsid."""
    url = "https://www.dns-shop.ru/product/043f7f7d8dd4d0a4/63-smartfon-apple-iphone-17-pro-512-gb-serebristyj/"

    # Получаем свежий qrator_jsid
    qrator_id = get_qrator_cookie()
    if not qrator_id:
        print("[DNS] Не удалось получить qrator_jsid")
        return None

    cookies = {"qrator_jsid": qrator_id}

    try:
        response = requests.get(url, headers=HEADERS, cookies=cookies, timeout=10)
        print(f"[DNS] HTTP статус: {response.status_code}, длина HTML: {len(response.text)}")

        if response.status_code != 200:
            print(f"[DNS] Статус {response.status_code} — cookie не сработал или истёк")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("div", class_="product-buy__price")

        if price_tag:
            price = int(re.sub(r"[^\d]", "", price_tag.text))
            return price

        print("[DNS] Тег с ценой не найден. Сохраняю HTML в debug_dns.html")
        with open("debug_dns.html", "w", encoding="utf-8") as f:
            f.write(response.text)
    except Exception as e:
        print(f"[DNS] Ошибка: {e}")
    return None
 заканчивается DNS
 '''


def parse_05ru() -> int | None:
    """Парсит цену на 05.ru через Playwright (сайт защищён JS-челленджем ABOT)."""
    url = "https://05.ru/cat/396f7486/p/smartfon-apple-iphone-17-pro-12-gb-512-gb-beliy-bez-rustore-23982/"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # False, если headless блокируется
            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")

            # Ждём, пока JS выполнит редирект и отрисует цену
            page.wait_for_selector("p.offer-seller__price", timeout=20000)
            text = page.locator("p.offer-seller__price").first.inner_text()
            browser.close()

        price = int(re.sub(r"[^\d]", "", text))
        return price
    except Exception as e:
        print(f"[05.ru] Ошибка: {e}")
    return None


def parse_real2() -> int | None:
    """Парсит цену на real2.ru (Tilda)."""
    url = "https://real2.ru/apple/tproduct/455809955903-smartfon-iphone-17-pro-512-gb-silver-sim"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 1. Цена в атрибуте data-product-price-def
        price_tag = soup.find("div", class_="js-product-price")
        if price_tag:
            price_str = price_tag.get("data-product-price-def")
            if price_str:
                price = int(re.sub(r"[^\d]", "", price_str))
                # Tilda хранит цену в копейках (микроединицах)
                if price > 1000000:
                    price = price // 10000
                return price
            # Если атрибута вдруг нет — берём текст
            price = int(re.sub(r"[^\d]", "", price_tag.text))
            return price

        # 2. Fallback: ищем по классу t-store__prod-popup__price-value
        price_tag = soup.find("div", class_="t-store__prod-popup__price-value")
        if price_tag:
            price = int(re.sub(r"[^\d]", "", price_tag.text))
            return price

        print("[real2] Тег с ценой не найден. Сохраняю HTML в debug_real2.html")
        with open("debug_real2.html", "w", encoding="utf-8") as f:
            f.write(response.text)
    except Exception as e:
        print(f"[real2] Ошибка: {e}")
    return None


def parse_citilink() -> int | None:
    """Парсит цену в Ситилинк через Playwright (Qrator, нужен реальный браузер)."""
    url = "https://www.citilink.ru/product/smartfon-apple-iphone-17-pro-a3523-512gb-serebristyi-3g-4g-1sim-6-3-12-2183033/properties/"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # как у М.Видео и 05.ru
            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            # Ждём, пока Qrator пропустит и цена отрисуется
            page.wait_for_selector("span[class*='MainPriceNumber']", timeout=20000)
            text = page.locator("span[class*='MainPriceNumber']").first.inner_text()
            browser.close()

        price = int(re.sub(r"[^\d]", "", text))
        return price
    except Exception as e:
        print(f"[citilink] Ошибка: {e}")
    return None