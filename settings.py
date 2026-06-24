import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-this-in-production-use-a-long-random-string')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
_trusted_hosts = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '').split(',') if h.strip() and h.strip() != '*']
CSRF_TRUSTED_ORIGINS = (
    [f"https://{h}" for h in os.environ.get('REPLIT_DOMAINS', '').split(',') if h]
    + [f"https://{h}" for h in _trusted_hosts]
    + ['http://localhost:8000', 'http://127.0.0.1:8000']
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registrations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # for static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hiddenbraj.urls'

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
                'hiddenbraj.context_processors.google_maps',
            ],
        },
    },
]

WSGI_APPLICATION = 'hiddenbraj.wsgi.application'

# Database — SQLite for dev, PostgreSQL for production
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin token for the custom admin panel (separate from Django admin)
ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'hiddenbraj2026')

# Email configuration (optional)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('GMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('GMAIL_PASS', '')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', '')

# Google Sheets webhook (optional)
GOOGLE_SHEET_WEBHOOK = os.environ.get('GOOGLE_SHEET_WEBHOOK', '')

# WhatsApp notifications via CallMeBot (optional)
# Setup: Save +34 644 56 78 10 as "CallMeBot", send "I allow callmebot to send me messages",
# receive your API key, then set these two env vars.
WHATSAPP_NUMBER  = os.environ.get('WHATSAPP_NUMBER', '')   # e.g. 919876543210 (no + or spaces)
WHATSAPP_API_KEY = os.environ.get('WHATSAPP_API_KEY', '')

# Google Maps API key (optional — for interactive map on homepage)
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
