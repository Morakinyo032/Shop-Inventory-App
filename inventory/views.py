from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ItemForm, StockMovementForm
from .models import Item, StockMovement


@login_required
def dashboard(request):
    items = Item.objects.select_related("category").all()
    low_stock_items = [i for i in items if i.is_low_stock]
    recent_movements = StockMovement.objects.select_related("item", "recorded_by")[:10]
    context = {
        "total_items": items.count(),
        "total_stock_value": sum(i.stock_value for i in items),
        "low_stock_items": low_stock_items,
        "low_stock_count": len(low_stock_items),
        "recent_movements": recent_movements,
    }
    return render(request, "inventory/dashboard.html", context)


@login_required
def item_list(request):
    query = request.GET.get("q", "").strip()
    items = Item.objects.select_related("category").all()
    if query:
        items = items.filter(Q(name__icontains=query) | Q(sku__icontains=query))
    return render(request, "inventory/item_list.html", {"items": items, "query": query})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    movements = item.movements.select_related("recorded_by")[:20]
    return render(request, "inventory/item_detail.html", {"item": item, "movements": movements})


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'"{item.name}" was added to inventory.')
            return redirect("inventory:item_detail", pk=item.pk)
    else:
        form = ItemForm()
    return render(request, "inventory/item_form.html", {"form": form, "title": "Add Item"})


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" was updated.')
            return redirect("inventory:item_detail", pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, "inventory/item_form.html", {"form": form, "title": f"Edit {item.name}"})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        name = item.name
        item.delete()
        messages.success(request, f'"{name}" was deleted.')
        return redirect("inventory:item_list")
    return render(request, "inventory/item_confirm_delete.html", {"item": item})


@login_required
def movement_create(request):
    initial = {}
    item_id = request.GET.get("item")
    if item_id:
        initial["item"] = item_id

    if request.method == "POST":
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.recorded_by = request.user
            movement.save()
            messages.success(
                request,
                f"Recorded {movement.get_movement_type_display()} of {movement.quantity} for {movement.item.name}.",
            )
            return redirect("inventory:item_detail", pk=movement.item.pk)
    else:
        form = StockMovementForm(initial=initial)
    return render(request, "inventory/movement_form.html", {"form": form})


@login_required
def movement_list(request):
    movements = StockMovement.objects.select_related("item", "recorded_by").all()
    return render(request, "inventory/movement_list.html", {"movements": movements})


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added.")
            return redirect("inventory:item_create")
    else:
        form = CategoryForm()
    return render(request, "inventory/category_form.html", {"form": form})
