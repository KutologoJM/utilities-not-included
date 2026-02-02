# settings/dev.py
from .base import *  # noqa: F403

DEBUG = os.getenv("DEBUG_DEV")
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INTERNAL_IPS = [
    "127.0.0.1",
]


INSTALLED_APPS += ["debug_toolbar", "django_browser_reload", "django_watchfiles",]  # noqa: F405

MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
MIDDLEWARE.insert(
    3, "django_browser_reload.middleware.BrowserReloadMiddleware"
)  # noqa: F405

DATABASES = {
    "default": dj_database_url.config(  # noqa: F405
        default=os.getenv("DATABASE_URL_DEV"),  # noqa: F405
        conn_max_age=600,
        ssl_require=True,
    )
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
