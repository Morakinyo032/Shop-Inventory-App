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

## Environment variables

The app reads these from the environment (all optional locally — sensible
defaults are used in DEBUG mode):

| Variable | Purpose | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | random 50-char string |
| `DJANGO_DEBUG` | `True`/`False` | `False` in production |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `yourusername.pythonanywhere.com` |
| `DJANGO_EMAIL_BACKEND` | Email backend | `django.core.mail.backends.smtp.EmailBackend` |
| `DJANGO_EMAIL_HOST` | SMTP host | `smtp.gmail.com` |
| `DJANGO_EMAIL_PORT` | SMTP port | `587` |
| `DJANGO_EMAIL_USE_TLS` | TLS on/off | `True` |
| `DJANGO_EMAIL_HOST_USER` | SMTP username/email | `you@gmail.com` |
| `DJANGO_EMAIL_HOST_PASSWORD` | SMTP password (use an **App Password** for Gmail) | `xxxx xxxx xxxx xxxx` |
| `DJANGO_DEFAULT_FROM_EMAIL` | From address | `you@gmail.com` |
| `DJANGO_ADMINS` | Who receives low-stock alerts, `Name:email` pairs comma-separated | `Owner:owner@example.com,Manager:mgr@example.com` |

In development, `DJANGO_EMAIL_BACKEND` defaults to the console backend, so
low-stock emails just print to your terminal instead of actually sending —
handy for testing without SMTP setup.

## Deploying to PythonAnywhere

1. Create a **new** PythonAnywhere account (or a new Web app if your plan allows
   more than one) since your existing account/app is already in use.
2. Open a Bash console on PythonAnywhere and clone your repo:
   ```bash
   git clone <your-repo-url>
   cd shopinventory
   ```
3. Create a virtualenv and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 shopinventory-env
   pip install -r requirements.txt
   ```
4. In the **Web** tab, create a new web app → Manual configuration → matching
   Python version → point the virtualenv path to the one you just created.
5. Edit the WSGI file PythonAnywhere gives you so it points to
   `shopinventory.wsgi.application`, and add your project directory to
   `sys.path`.
6. Set environment variables in the **Web** tab's "Environment variables"
   section (or a `.env` loaded at the top of `wsgi.py` — PythonAnywhere free
   tier supports the Environment variables box directly). At minimum set
   `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and
   `DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com`.
7. In the Bash console:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```
8. In the **Web** tab, add static/media file mappings:
   - URL `/static/` → Directory `/home/yourusername/shopinventory/staticfiles`
   - URL `/media/` → Directory `/home/yourusername/shopinventory/media`
   (The second mapping is required for uploaded product photos to display.)
9. Reload the web app.

## Demo flow (for the 2–3 min demo video)

1. Log in.
2. Show the dashboard (empty state).
3. Add 2–3 items with different reorder levels.
4. Record a Stock In movement — show quantity update.
5. Record a Stock Out that drops an item below its reorder level — show the
   low-stock badge appear on the dashboard and item list, and show the email
   alert (console output locally, or an inbox if SMTP is configured).
6. Attempt a Stock Out larger than available quantity — show it's blocked.
7. Search for an item by name/SKU.
8. Briefly show the Django admin.

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
