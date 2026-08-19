from django.core.exceptions import ValidationError
from django.core.mail import mail_admins
from django.db import models, transaction
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField("SKU", max_length=50, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(
        default=5, help_text="Alert is triggered when quantity falls to or below this level."
    )
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    supplier = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to="item_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse("inventory:item_detail", args=[self.pk])

    @property
    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    @property
    def stock_value(self):
        return self.quantity * self.unit_price

    def send_low_stock_alert(self):
        """Emails site admins (settings.ADMINS) when stock hits/falls below reorder level."""
        mail_admins(
            subject=f"Low stock alert: {self.name}",
            message=(
                f"{self.name} (SKU: {self.sku}) is low on stock.\n\n"
                f"Current quantity: {self.quantity}\n"
                f"Reorder level: {self.reorder_level}\n\n"
                f"Please restock soon."
            ),
            fail_silently=True,
        )


class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    MOVEMENT_TYPES = [
        (IN, "Stock In"),
        (OUT, "Stock Out"),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.item.name} ({self.quantity})"

    def clean(self):
        if self.movement_type == self.OUT and self.quantity > self.item.quantity:
            raise ValidationError(
                f"Cannot remove {self.quantity} units - only {self.item.quantity} in stock."
            )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                item = Item.objects.select_for_update().get(pk=self.item_id)
                was_low = item.is_low_stock
                if self.movement_type == self.IN:
                    item.quantity += self.quantity
                else:
                    item.quantity -= self.quantity
                item.save(update_fields=["quantity", "updated_at"])
                if item.is_low_stock and not was_low:
                    item.send_low_stock_alert()
