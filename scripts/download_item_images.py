"""
download_item_images.py

Downloads placeholder product images for the 10 seeded inventory items,
saved as JPGs ready to upload via the item edit form.

Uses placehold.co - a free, no-signup, no-API-key placeholder image
generator. Each image is a colored box with the product name on it.
Swap these for real photos later once you're photographing real stock.
"""

import os
import requests

# (SKU, product name, background hex color)
ITEMS = [
    ("GRN-001", "Rice 50kg Bag",     "8B5E34"),
    ("OIL-001", "Vegetable Oil 5L",  "E8A33D"),
    ("BEV-001", "Coca-Cola 50cl",    "C0392B"),
    ("DRY-001", "Peak Milk 400g",    "3B7DD8"),
    ("NDL-001", "Indomie Noodles",   "F1C40F"),
    ("GRN-002", "Golden Penny Semo", "D2B48C"),
    ("TOI-001", "Dettol Soap",       "1ABC9C"),
    ("GRN-003", "Dangote Sugar 1kg", "ECF0F1"),
    ("SPC-001", "Maggi Cubes",       "27AE60"),
    ("BEV-002", "Eva Water 75cl",    "5DADE2"),
]

OUTPUT_DIR = "sample_item_photos"
IMAGE_SIZE = "600x600"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for sku, name, color in ITEMS:
        text = name.replace(" ", "+")
        url = f"https://placehold.co/{IMAGE_SIZE}/{color}/FFFFFF.jpg?text={text}&font=roboto"

        filepath = os.path.join(OUTPUT_DIR, f"{sku}.jpg")

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(resp.content)
            print(f"  + Downloaded {filepath}")
        except requests.RequestException as e:
            print(f"  ! Failed for {sku} ({name}): {e}")

    print(f"\nDone. Images saved in ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
