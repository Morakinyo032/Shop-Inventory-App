from django import forms
from .models import Item, StockMovement, Category


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "sku", "category", "quantity", "reorder_level", "unit_price", "supplier"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "supplier": forms.TextInput(attrs={"class": "form-control"}),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ["item", "movement_type", "quantity", "note"]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select"}),
            "movement_type": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "note": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional note"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get("item")
        quantity = cleaned_data.get("quantity")
        movement_type = cleaned_data.get("movement_type")
        if item and quantity and movement_type == StockMovement.OUT and quantity > item.quantity:
            raise forms.ValidationError(
                f"Cannot remove {quantity} units — only {item.quantity} of {item.name} in stock."
            )
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
