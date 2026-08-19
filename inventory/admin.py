from django.contrib import admin
from .models import Category, Item, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "category", "quantity", "reorder_level", "unit_price", "is_low_stock"]
    list_filter = ["category"]
    search_fields = ["name", "sku"]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["item", "movement_type", "quantity", "recorded_by", "timestamp"]
    list_filter = ["movement_type", "timestamp"]
    search_fields = ["item__name", "item__sku"]
