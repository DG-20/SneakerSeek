from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("register", views.register, name="register"),
    path("search_view", views.search_view, name="search_view"),
    path("results/<str:pk>", views.results, name="results"),
    path("product/<str:pk>", views.product, name="product"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("settings", views.settings, name="settings"),
    path("profile", views.profile, name="profile"),
]
