# Shop Inventory App (SD-11)

A lightweight inventory management system for small Nigerian shops. Built to solve
a simple, real problem: shops mismanage stock — no visibility into what's running
low until it's already out.

## Features

- **Items** — track name, SKU, category, quantity, reorder level, unit price,
  supplier, and an optional product photo
- **Stock movements** — record Stock In / Stock Out with an audit trail (who, when, why)
- **Low-stock alerts** — dashboard warnings + automatic email when quantity drops
  to or below an item's reorder level
- **Oversell protection** — can't record a Stock Out larger than what's in stock
- **Search** — quick lookup by item name or SKU
- **Auth** — login required for all inventory pages (single-shop, staff login)
- **Admin panel** — Django admin for power-user data management

## Tech stack

- Django 5.1 (Python)
- SQLite (default; swappable for Postgres)
- Bootstrap 5 (CDN, no build step)

## Local setup

```bash
git clone <your-repo-url>
cd shopinventory
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in with the superuser you created.


## Project structure

```
shopinventory/
├── inventory/          # the app: models, views, forms, admin, urls
├── shopinventory/       # project settings, root urls, wsgi/asgi
├── templates/           # base.html, registration/, inventory/
├── static/               # static assets (currently empty, Bootstrap via CDN)
├── manage.py
├── requirements.txt
└── README.md
```
