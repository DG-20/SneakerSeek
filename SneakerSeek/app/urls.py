from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("search_view", views.search_view, name="search_view"),
    path("results/<str:pk>", views.results, name="results"),
    path("product/<str:pk>", views.product, name="product"),
]
