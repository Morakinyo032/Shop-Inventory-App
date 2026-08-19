"""
Django settings for shopinventory project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Core / security
# --------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-w0*4mh=p!w25ld+&@huoxgg=3oe&yi%$1cag6^+ygj4*aq^@g_",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()
]

# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'inventory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopinventory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shopinventory.wsgi.application'

# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------------------------------------------------------------
# Password validation
# --------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Static & media
# --------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------------------
# Auth redirects
# --------------------------------------------------------------------------
MESSAGE_TAGS = {
    40: 'danger',  # messages.ERROR
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inventory:dashboard'
LOGOUT_REDIRECT_URL = 'login'

# --------------------------------------------------------------------------
# Email (low-stock alerts)
# Set these as environment variables in production (PythonAnywhere: use a
# .env file or the "Environment variables" section of the Web tab).
# For Gmail, use an App Password, not your normal password.
# --------------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("DJANGO_EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DJANGO_DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# mail_admins() sends low-stock alerts to everyone listed here.
ADMINS = [
    tuple(pair.split(":", 1))
    for pair in os.environ.get("DJANGO_ADMINS", "Shop Owner:owner@example.com").split(",")
    if ":" in pair
]
