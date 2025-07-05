from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    re_path(r"^healthz/ready/?$", views.Healthcheck.as_view()),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/host/", include("users.urls")),
]
