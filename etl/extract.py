from pathlib import Path

import pandas as pd

dir = Path(__file__).resolve().parents[1] / "fklubdata"


def extract():
    member = pd.read_csv(dir / "member.csv", sep=";")
    sale = pd.read_csv(dir / "sale.csv", sep=";")
    location = pd.read_csv(dir / "room.csv", sep=";")
    product = pd.read_csv(dir / "product.csv", sep=";")
    category = pd.read_csv(dir / "category.csv", sep=";")
    product_category = pd.read_csv(dir / "product_categories.csv", sep=";")
    old_price = pd.read_csv(dir / "oldprice.csv", sep=";")
    return {
        "member": member,
        "sale": sale,
        "location": location,
        "product": product,
        "category": category,
        "product_category": product_category,
        "old_price": old_price,
    }
