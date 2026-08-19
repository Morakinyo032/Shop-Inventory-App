from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("items/", views.item_list, name="item_list"),
    path("items/add/", views.item_create, name="item_create"),
    path("items/<int:pk>/", views.item_detail, name="item_detail"),
    path("items/<int:pk>/edit/", views.item_update, name="item_update"),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),
    path("movements/", views.movement_list, name="movement_list"),
    path("movements/add/", views.movement_create, name="movement_create"),
    path("categories/add/", views.category_create, name="category_create"),
]
