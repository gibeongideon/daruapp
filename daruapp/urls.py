"""daruapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from decouple import config

admin.site.site_header = "DaruApp Admin"

urlpatterns = [
    path(
        config("SECRET_ADMIN_URL", default="dadmin") + "/admin/",
        admin.site.urls),
    path("", include("dashboard.urls", namespace="dashboard")),
    path("user/", include("users.urls", namespace="users")),
    path("daru_wheel/", include("daru_wheel.urls", namespace="daru_wheel")),
    path("account/", include("account.urls", namespace="account")),
    path("pesa/", include("mpesa_api.core.urls", "mpesa")),
    path('paypal/', include('paypal.standard.ipn.urls')), ]
