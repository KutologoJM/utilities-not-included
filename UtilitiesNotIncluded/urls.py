"""
URL configuration for UtilitiesNotIncluded project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from health_check.views import HealthCheckView

from accounts.views import Dashboard


urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    # Health Check docs https://codingjoe.dev/django-health-check/
    path(
        f"health/{settings.HEALTH_CHECK_TOKEN}/",
        HealthCheckView.as_view(
            checks=[
                "health_check.DNS",
                "health_check.Cache",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                # 3rd party checks
                "health_check.contrib.psutil.Battery",
                "health_check.contrib.psutil.CPU",
                "health_check.contrib.psutil.Memory",
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Temperature",
                # "health_check.contrib.celery.Ping",
                # "health_check.contrib.redis.Redis",
                # "health_check.contrib.atlassian.Cloudflare",
                "health_check.contrib.atlassian.Render",
            ]
        ),
    ),
    path("accounts/", include("accounts.urls")),
    path("food_manager/", include("food_manager.urls")),
    path("colony_manager/", include("colony_manager.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path(
            "__debug__/", include(debug_toolbar.urls)
        ),  # This registers the 'djdt' namespace
        path("__reload__/", include("django_browser_reload.urls")),
    ] + urlpatterns
