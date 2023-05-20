import os
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("SECRET_KEY")

CORS_ALLOW_HEADERS = ['*']

CORS_ALLOW_ALL_ORIGINS = True




ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}