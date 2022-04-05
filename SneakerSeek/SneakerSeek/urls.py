"""SneakerSeek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    path("get_all_cities/", api.get_all_cities),
    path(
        "get_shoes_by_params/<str:brand>/<str:gender>/<str:type>/<str:size>/<str:condition>/<str:max_price>/<str:city>/<str:quadrant>/",
        api.get_shoes_by_params,
    ),
    path("get_shoe_by_id/<str:shoe_id>/", api.get_shoe_by_id),
    path(
        "get_shoes_by_username/<str:username>/",
        api.get_shoes_by_username,
    ),
    path(
        "interested_in/<str:shoe_id>/<str:username>/",
        api.interested_in,
    ),
    path(
        "get_interested_by_shoe_id/<str:shoe_id>/",
        api.get_interested_by_shoe_id,
    ),
    path("delete_shoe/<str:shoe_id>/", api.delete_shoe),
    path("get_all_shoes/", api.get_all_shoes),
    path(
        "upload_shoe/<str:brand>/<str:size>/<str:type>/<str:name>/<str:price>/<str:gender>/<str:year>/<str:condition>/<str:city>/<str:quadrant>/<str:image_url>/<str:seller_username>/",
        api.upload_shoe,
    ),
    path(
        "update_shoe/<str:shoe_id>/<str:brand>/<str:size>/<str:type>/<str:name>/<str:price>/<str:gender>/<str:year>/<str:condition>/<str:city>/<str:quadrant>/",
        api.update_shoe,
    ),
]
