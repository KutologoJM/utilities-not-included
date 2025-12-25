# settings/local.py
from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INTERNAL_IPS = [
    "127.0.0.1",
]


INSTALLED_APPS += ["debug_toolbar", "django_browser_reload"]

MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.insert(3, "django_browser_reload.middleware.BrowserReloadMiddleware")

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL_DEV"),
        conn_max_age=600,
        ssl_require=True,
    )
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
