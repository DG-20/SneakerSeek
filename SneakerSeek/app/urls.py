from django.urls import path, include
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
    path("sell_shoe", views.sell_shoe, name="sell_shoe"),
    path("my_shoes", views.my_shoes, name="my_shoes"),
    path("manage_users", views.manage_users, name="manage_users"),
    path("edit_shoe/<str:pk>", views.edit_shoe, name="edit_shoe"),
]
