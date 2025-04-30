from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from arenabuilds import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
