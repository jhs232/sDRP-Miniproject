from datetime import date
import pandas as pd


def transform(data):
    data["member"] = transform_member(data["member"])
    data["location"] = transform_location(data["location"])

    return data


def transform_member(member_data):
    valid_genders = {"M", "F", "U"}
    current_year = date.today().year
    member_data = member_data[
        member_data["gender"].isin(valid_genders)
        & member_data["year"].between(1976, current_year)
    ].copy()

    member_data = member_data[["id", "year", "gender"]]

    member_data["gender"] = member_data["gender"].map(
        {
            "M": "Male",
            "F": "Female",
            "U": "Unknown",
        }
    )
    return member_data


def transform_location(location_data):
    location_data = location_data[["id", "name"]]

    location_data["is_event"] = location_data["name"].map(
        {
            "Websalg": False,
            "cs": False,
            "math": False,
            "Fyttetur": True,
            "Julefrokost": True,
            "FooBar": True,
            "Sportsdag": True,
            "Ad hoc - FRB 7A Kæld": True,
            "FRB 7A": False,
        }
    )

    unknown = location_data["is_event"].isna()
    if unknown.any():
        names = location_data.loc[unknown, "name"].unique().tolist()
        raise ValueError(f"Unknown room(s): {names}")

    return location_data


def transform_product(product_data):
    product_data = product_data[["id", "name", "price", "alcohol_content_ml"]]

    # Map alcohol_content_ml > 0 to contains_alcohol = true
    product_data["contains_alcohol"] = product_data["alcohol_content_ml"] > 0
    unknown_alcohol_content = product_data["alcohol_content_ml"].isna()
    if unknown_alcohol_content.any():
        names = product_data.loc[unknown_alcohol_content, "name"].unique().tolist()
        raise ValueError(f"Products with unknown alcohol content: {names}")

    # Map product names to known brands
    known_brands = {
        "Barebells",
        "Brooklyn",
        "Budget",
        "Budweiser",
        "Burn",
        "Carlsberg",
        "Cocio",
        "Corona",
        "Cult",
        "Cultura",
        "Franziskaner",
        "Grimbergen",
        "Harboe",
        "Haribo",
        "Jolt",
        "Kongens Bryghus",
        "Little Miracles",
        "Matilde",
        "Monster",
        "Nestea",
        "Red Bull",
        "Schweppes",
        "Somersby",
        "Staropramen",
        "Tuborg",
        "Vitamin Well",
        "X-Ray",
        "Xide",
    }
    brand_overrides = {
        "Somersby/Xide": "Mixed",
        "Corona Extra & Franziskaner Dunk": "Mixed",
        "150ml Cultura": "Cultura",
        "½L drikkecultura": "Cultura",
    }
    product_data["brand"] = product_data["name"].map(
        lambda name: get_brand(name, known_brands, brand_overrides)
    )

    # Map names to volumes, where possible
    known_volumes = {
        "½L": 500,
        "¼L": 250,
        "1L": 1000,
        "150ml": 150,
        "200ml": 200,
        "250 ml": 250,
        "0,5 L": 500,
        "1,5L": 1500,
        "2 L": 2000,
        "0,8L": 800,
        "0.375L": 375,
    }
    volume_overrides = {
        "½L Skummetmælk (2x¼)": 500,
        "½L Kærnemælk (2x¼)": 500,
        "½L Øko Skummet (2x¼)": 500,
        "24 x 0,5 L sodavand uden pant": 12000,
    }
    product_data["volume"] = product_data["name"].map(
        lambda name: get_volume(name, known_volumes, volume_overrides)
    )


def get_brand(name, known_brands, brand_overrides):
    if pd.isna(name):
        return "Unknown"

    if name in brand_overrides:
        return brand_overrides[name]

    matches = [brand for brand in known_brands if brand.casefold() in name.casefold()]

    if len(matches) > 1:
        raise ValueError(f"Multiple brands in {name!r}: {sorted(matches)}")

    return matches[0] if matches else "Unknown"


def get_volume(name, known_volumes, volume_overrides):
    if pd.isna(name):
        return "Unknown"

    if name in volume_overrides:
        return volume_overrides[name]

    matches = {
        ml
        for volume_text, ml in known_volumes.items()
        if volume_text.casefold() in name.casefold()
    }

    if len(matches) > 1:
        raise ValueError(f"Multiple volumes in {name!r}: {sorted(matches)}")

    return next(iter(matches)) if matches else "Unknown"
