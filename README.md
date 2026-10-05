# 📱 iPhone 17 Pro 512GB Silver — Парсер динамики цен

Пет-проект на Python: собирает цены на **iPhone 17 Pro 512GB Silver** с пяти российских магазинов, сохраняет историю и показывает динамику на веб-странице с графиком.

**🌐 Живая демонстрация:** [larawagner008.github.io/iphone17Pro_parser](https://larawagner008.github.io/iphone17Pro_parser/)

---

## ✨ Что умеет проект

- 🔍 **Парсит 5 магазинов** с разными техниками (requests + JSON, requests + HTML, Playwright)
- 💾 **Сохраняет историю цен** в JSON-файл
- 📊 **Визуализирует динамику** на графике через Chart.js
- 🤖 **Автоматически обновляется** раз в день через GitHub Actions
- 🌐 **Публикует результат** на GitHub Pages — без сервера и хостинга

---

## 🏪 Источники и техники парсинга

| Магазин | Техника | Статус в Actions |
|---|---|---|
| **re-store** | `requests` + JSON из `window.__INITIAL_STATE__` | ✅ работает |
| **05.ru** | Playwright (обход ABOT JS-челленджа) | ✅ работает |
| **real2.ru** | `requests` + BeautifulSoup (Tilda) | ✅ работает |
| **М.Видео** | Playwright (Angular + антибот) | ⚠️ блокируется IP GitHub Actions |
| **Citilink** | Playwright (Qrator + gRPC-web) | ⚠️ блокируется IP GitHub Actions |

**Почему М.Видео и Citilink не работают в облаке:** их антибот-системы блокируют IP-адреса датацентров (GitHub Actions работает на Amazon AWS, США). Локально с домашнего IP все пять магазинов парсятся успешно. Для стабильной работы в облаке нужны резидентные прокси.

---

## 🛠️ Стек технологий

- **Python 3.12** — язык проекта
- **requests** — HTTP-запросы
- **BeautifulSoup4** — парсинг HTML
- **Playwright** — headless-браузер для JS-сайтов
- **Chart.js** — график на фронтенде
- **GitHub Actions** — автоматизация по расписанию
- **GitHub Pages** — публикация статической страницы

---

## 📁 Структура проекта
```
iphone17Pro_parser/
├── .github/
│ └── workflows/
│ └── scrape.yml # Workflow для автоматического парсинга
├── data/
│ └── prices.json # История цен (обновляется Actions)
├── .gitignore
├── index.html # Страница с графиком и таблицей
├── main.py # Точка входа — запускает парсеры
├── parsers.py # Модуль с парсерами 5 магазинов
├── requirements.txt # Зависимости
└── README.md # Этот файл
```

---

## 🚀 Как запустить локально

### 1. Клонировать репозиторий

```bash
git clone https://github.com/LaraWagner008/iphone17Pro_parser.git
cd iphone17Pro_parser
```

### 2. Создать виртуальное окружение
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Запустить парсер

```bash
python main.py
```

Результат появится в data/prices.json.

### 5. Посмотреть страницу с графиком

Открыть index.html в браузере.

## ⚙️ Как работает автоматизация

- Workflow .github/workflows/scrape.yml запускается каждый день в 06:00 UTC (09:00 МСК):

1. GitHub Actions запускает python main.py в облаке.

2. Парсер собирает цены с работающих магазинов.

3. Обновлённый data/prices.json коммитится обратно в репозиторий.

4. GitHub Pages автоматически пересобирает страницу с новыми данными.

- Можно запускать вручную: Actions → Scrape prices and deploy → Run workflow.

## 📈 Что показывает страница

- Таблица — последняя цена в каждом магазине и время обновления.

- График — линии по магазинам, каждая точка = один запуск парсера.