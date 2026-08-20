from django.core.management.base import BaseCommand
from inventory.models import Category, Item


SAMPLE_ITEMS = [
    {
        "name": "Rice 50kg Bag (Local)",
        "sku": "GRN-001",
        "category": "Grains & Staples",
        "quantity": 12,
        "reorder_level": 5,
        "unit_price": 45000,
        "supplier": "Mile 12 Grains Depot",
    },
    {
        "name": "Vegetable Oil 5L (Kings)",
        "sku": "OIL-001",
        "category": "Cooking Oil",
        "quantity": 20,
        "reorder_level": 8,
        "unit_price": 9500,
        "supplier": "PZ Cussons Distributor",
    },
    {
        "name": "Coca-Cola 50cl (Pack of 12)",
        "sku": "BEV-001",
        "category": "Beverages",
        "quantity": 30,
        "reorder_level": 10,
        "unit_price": 3600,
        "supplier": "NBC Depot Lagos",
    },
    {
        "name": "Peak Milk Powder 400g",
        "sku": "DRY-001",
        "category": "Dairy",
        "quantity": 25,
        "reorder_level": 10,
        "unit_price": 2800,
        "supplier": "FrieslandCampina Distributor",
    },
    {
        "name": "Indomie Noodles (Carton of 40)",
        "sku": "NDL-001",
        "category": "Noodles & Pasta",
        "quantity": 15,
        "reorder_level": 5,
        "unit_price": 8500,
        "supplier": "Dufil Prima Foods",
    },
    {
        "name": "Golden Penny Semovita 1kg",
        "sku": "GRN-002",
        "category": "Grains & Staples",
        "quantity": 18,
        "reorder_level": 6,
        "unit_price": 1400,
        "supplier": "Flour Mills of Nigeria",
    },
    {
        "name": "Dettol Soap (Pack of 6)",
        "sku": "TOI-001",
        "category": "Toiletries",
        "quantity": 22,
        "reorder_level": 8,
        "unit_price": 3200,
        "supplier": "Reckitt Benckiser Distributor",
    },
    {
        "name": "Dangote Sugar 1kg",
        "sku": "GRN-003",
        "category": "Grains & Staples",
        "quantity": 4,
        "reorder_level": 10,
        "unit_price": 1600,
        "supplier": "Dangote Sugar Refinery",
    },
    {
        "name": "Maggi Cubes (Carton)",
        "sku": "SPC-001",
        "category": "Spices & Seasoning",
        "quantity": 10,
        "reorder_level": 4,
        "unit_price": 5200,
        "supplier": "Nestle Distributor",
    },
    {
        "name": "Eva Bottled Water 75cl (Pack of 12)",
        "sku": "BEV-002",
        "category": "Beverages",
        "quantity": 3,
        "reorder_level": 6,
        "unit_price": 1500,
        "supplier": "FUTMINNA Water Depot",
    },
]


class Command(BaseCommand):
    help = "Seeds the database with 10 sample shop items for local testing/demo purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing items before seeding (use with care).",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            deleted, _ = Item.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing item(s)."))

        created_count = 0
        updated_count = 0

        for data in SAMPLE_ITEMS:
            category, _ = Category.objects.get_or_create(name=data["category"])
            item, created = Item.objects.update_or_create(
                sku=data["sku"],
                defaults={
                    "name": data["name"],
                    "category": category,
                    "quantity": data["quantity"],
                    "reorder_level": data["reorder_level"],
                    "unit_price": data["unit_price"],
                    "supplier": data["supplier"],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + Created {item.name} ({item.sku})"))
            else:
                updated_count += 1
                self.stdout.write(f"  ~ Updated {item.name} ({item.sku})")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. {created_count} item(s) created, {updated_count} updated. "
                f"Photos were not set — add them via the UI (Edit item) if you want thumbnails."
            )
        )
