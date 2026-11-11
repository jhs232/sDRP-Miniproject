from datetime import date, timedelta, timezone
from enum import Enum
import pandas as pd


class Category(str, Enum):
    BEVERAGE = "Drikkevarer"
    FOOD = "Mad"
    EVENT = "Arrangementer"
    OTHER = "Øvrigt"


CATEGORY_CONSUMABLE = {
    Category.BEVERAGE: True,
    Category.FOOD: True,
    Category.EVENT: False,
    Category.OTHER: False,
}


class ProductType(str, Enum):
    SODA = "Sodavand"
    BEER = "Øl"
    WATER = "Vand"
    VITAMIN_WATER = "Vitaminvand"
    JUICE = "Juice og most"
    MILK = "Mælk"
    COCOA = "Kakao"
    COFFEE = "Kaffe"
    TEA = "Te og iste"
    ENERGY_DRINK = "Energidrik"
    SPORTS_PROTEIN_DRINK = "Sports- og proteindrik"
    WINE = "Vin"
    SPIRITS = "Spiritus"
    COCKTAIL = "Drinks"
    CIDER_ALCOPOP = "Cider og alkoholsodavand"
    MIXED_BEVERAGE = "Blandet drikkevare"
    UNKNOWN_BEVERAGE = "Ukendt drikkevare"
    SNACK = "Snack"
    MEAL = "Måltid"
    BREAD = "Brød"
    YOGHURT = "Yoghurt"
    TICKET = "Billet"
    GAME_CARD = "Spilleplade"
    MUG = "Krus"
    BOOK = "Bog"
    EQUIPMENT = "Udstyr"
    DEPOSIT = "Pant"
    FEE = "Gebyr"
    SERVICE = "Ydelse"
    TEST_PRODUCT = "Testprodukt"
    UNKNOWN = "Ukendt"


TYPE_CATEGORY = {
    ProductType.SODA: Category.BEVERAGE,
    ProductType.BEER: Category.BEVERAGE,
    ProductType.WATER: Category.BEVERAGE,
    ProductType.VITAMIN_WATER: Category.BEVERAGE,
    ProductType.JUICE: Category.BEVERAGE,
    ProductType.MILK: Category.BEVERAGE,
    ProductType.COCOA: Category.BEVERAGE,
    ProductType.COFFEE: Category.BEVERAGE,
    ProductType.TEA: Category.BEVERAGE,
    ProductType.ENERGY_DRINK: Category.BEVERAGE,
    ProductType.SPORTS_PROTEIN_DRINK: Category.BEVERAGE,
    ProductType.WINE: Category.BEVERAGE,
    ProductType.SPIRITS: Category.BEVERAGE,
    ProductType.COCKTAIL: Category.BEVERAGE,
    ProductType.CIDER_ALCOPOP: Category.BEVERAGE,
    ProductType.MIXED_BEVERAGE: Category.BEVERAGE,
    ProductType.UNKNOWN_BEVERAGE: Category.BEVERAGE,
    ProductType.SNACK: Category.FOOD,
    ProductType.MEAL: Category.FOOD,
    ProductType.BREAD: Category.FOOD,
    ProductType.YOGHURT: Category.FOOD,
    ProductType.TICKET: Category.EVENT,
    ProductType.GAME_CARD: Category.EVENT,
    ProductType.MUG: Category.OTHER,
    ProductType.BOOK: Category.OTHER,
    ProductType.EQUIPMENT: Category.OTHER,
    ProductType.DEPOSIT: Category.OTHER,
    ProductType.FEE: Category.OTHER,
    ProductType.SERVICE: Category.OTHER,
    ProductType.TEST_PRODUCT: Category.OTHER,
    ProductType.UNKNOWN: Category.OTHER,
}


PRODUCT_TYPE = {
    1: ProductType.TICKET,                 # Diverse - Fyttetur
    2: ProductType.MILK,                   # ½L Letmælk
    3: ProductType.MILK,                   # ¼L Letmælk
    4: ProductType.MILK,                   # ¼L Skummetmælk
    5: ProductType.MILK,                   # ¼L Kærnemælk
    6: ProductType.MILK,                   # ¼L Øko Letmælk
    7: ProductType.MILK,                   # ¼L Øko Skummetmælk
    8: ProductType.MILK,                   # ½L Skummetmælk (2x¼)
    9: ProductType.MILK,                   # 1L Letmælk
    10: ProductType.MILK,                  # ½L Kærnemælk (2x¼)
    11: ProductType.SODA,                  # ½L soda/nestea excl. pant
    12: ProductType.SODA,                  # ¼L Sodavand
    13: ProductType.BEER,                  # Øl(Guld & CB 47)
    14: ProductType.BEER,                  # Øl(Grøn/Classic/Rød/Rå)
    15: ProductType.BEER,                  # Øl(Corona)
    16: ProductType.COCOA,                 # Cocio
    17: ProductType.COCOA,                 # ½L Matilde cacao
    18: ProductType.MILK,                  # ¼L Øko Sødmælk
    19: ProductType.MILK,                  # ½L Øko Skummet (2x¼)
    20: ProductType.YOGHURT,               # 150ml Cultura
    21: ProductType.COCOA,                 # 200ml Mathilde Cacao
    22: ProductType.WINE,                  # 1 Flaske Rødvin
    23: ProductType.WINE,                  # 1 Flaske Hvidvin
    24: ProductType.YOGHURT,               # 150ml Yoghurt
    25: ProductType.MILK,                  # ¼L Øko Sødmælk
    26: ProductType.SNACK,                 # Popcorn
    27: ProductType.SNACK,                 # Chips
    28: ProductType.SNACK,                 # Saltstænger
    29: ProductType.BEER,                  # Øl(Tuborg Jul/Påske)
    30: ProductType.SODA,                  # Jolt
    31: ProductType.DEPOSIT,               # Pant B
    32: ProductType.MIXED_BEVERAGE,        # Kaffe/Choko(1 kop)
    33: ProductType.TEST_PRODUCT,          # dummyproduct
    34: ProductType.TEA,                   # Nestea
    35: ProductType.COFFEE,                # kaffe - ansat
    36: ProductType.COFFEE,                # kaffe - stud
    37: ProductType.SODA,                  # ½L soda incl. pant
    38: ProductType.JUICE,                 # Juice
    39: ProductType.COFFEE,                # Ansat KAFFE(1 kop)
    40: ProductType.UNKNOWN,               # Frisk luft v. BSS
    41: ProductType.SPIRITS,               # Snaps
    42: ProductType.BEER,                  # Limfjordsporter
    43: ProductType.MILK,                  # ½L drikkecultura
    44: ProductType.UNKNOWN,               # Søm
    45: ProductType.MILK,                  # ¼L Mælk
    46: ProductType.TICKET,                # F-Julefrokost
    47: ProductType.BEER,                  # Carlsberg 47
    48: ProductType.TICKET,                # F-sportsdag
    49: ProductType.UNKNOWN,               # Kandidat betaling
    50: ProductType.TICKET,                # Kandidatfest - gæst
    51: ProductType.TICKET,                # Fyttetur
    52: ProductType.SNACK,                 # Chokoladebar
    53: ProductType.UNKNOWN,               # Fisherman
    54: ProductType.BEER,                  # Ale No. 16
    55: ProductType.TICKET,                # Kort fyttetur - 2 dage
    56: ProductType.TICKET,                # FØLsmagning
    57: ProductType.BOOK,                  # F-bog (Se E1-214)
    58: ProductType.SNACK,                 # Slik, Haribo
    59: ProductType.EQUIPMENT,             # Rustfri stålvogn
    60: ProductType.TICKET,                # Indoor footballsæson
    61: ProductType.TICKET,                # F-acking
    62: ProductType.MUG,                   # F-Klub krus
    63: ProductType.COCKTAIL,              # Drink
    64: ProductType.WINE,                  # 1 flaske vin
    65: ProductType.BEER,                  # Fadøl
    66: ProductType.BEER,                  # Fadøl - Julebryg
    67: ProductType.MEAL,                  # Poelse med broed
    68: ProductType.MEAL,                  # Fransk Hotdog
    1767: ProductType.CIDER_ALCOPOP,       # Somersby/Xide
    1768: ProductType.JUICE,               # Æblemost
    1769: ProductType.COCKTAIL,            # Æblemost m. en enkelt
    1770: ProductType.COCKTAIL,            # Æblemost m. dobbelt
    1771: ProductType.UNKNOWN,             # Island TILBUD!
    1772: ProductType.FEE,                 # Adm Gebyr
    1773: ProductType.BEER,                # KB Juleøl (hvidtøl)
    1774: ProductType.BEER,                # F (oel)
    1775: ProductType.BEER,                # Fadøl i personligt glas
    1776: ProductType.BEER,                # Dåseøl + Grimbergen
    1777: ProductType.BEER,                # Lager/Special/Elefant
    1778: ProductType.TICKET,              # Feaster
    1779: ProductType.BEER,                # 2xJuleøl
    1780: ProductType.BEER,                # Limfjordsporter Fad
    1781: ProductType.TICKET,              # Famlefest
    1782: ProductType.TICKET,              # Special Hyttetur
    1783: ProductType.BEER,                # Øko Humle/Porse Guld/Øko Påske
    1784: ProductType.UNKNOWN,             # Æ Kas Kurwand
    1785: ProductType.GAME_CARD,           # Bingo Plader
    1786: ProductType.GAME_CARD,           # 3x Bingo Plader
    1787: ProductType.ENERGY_DRINK,        # Burn Shot
    1789: ProductType.UNKNOWN,             # Fames
    1790: ProductType.ENERGY_DRINK,        # Red Bull
    1791: ProductType.ENERGY_DRINK,        # Cult Cola / Cult
    1792: ProductType.TICKET,              # F-sportsdag + mad
    1793: ProductType.BEER,                # ØKO Humle
    1794: ProductType.BEER,                # Tuborg Lime Cut
    1795: ProductType.SODA,                # Schweppes Ginger Ale
    1796: ProductType.JUICE,               # Budget Juice (250 ml)
    1797: ProductType.TICKET,              # Fastelavn
    1798: ProductType.UNKNOWN_BEVERAGE,    # BEO*/Copenhagen
    1799: ProductType.ENERGY_DRINK,        # One EngergyDrink
    1800: ProductType.ENERGY_DRINK,        # X-Ray
    1801: ProductType.MEAL,                # F-Kult Meat Pie
    1802: ProductType.COCKTAIL,            # morgan + cola
    1803: ProductType.BEER,                # Fadøl normal/påske (sw system)
    1804: ProductType.ENERGY_DRINK,        # Burn Energy - Lagersalg
    1805: ProductType.UNKNOWN,             # Fragelse
    1806: ProductType.SPIRITS,             # Vodka
    1807: ProductType.BEER,                # Julemumme - Kongens Bryghus
    1808: ProductType.BEER,                # Øl(Jakobsen Ale)
    1809: ProductType.BEER,                # Carlsberg Christmas Ale
    1810: ProductType.UNKNOWN,             # Stripper Kassen
    1811: ProductType.TICKET,              # Gratis FooBar
    1812: ProductType.MUG,                 # Ølkrus
    1813: ProductType.UNKNOWN_BEVERAGE,    # HARBOE - ½L Vand excl. pant
    1814: ProductType.JUICE,               # Juice 1,5L
    1815: ProductType.COCOA,               # Kakao 1L
    1816: ProductType.JUICE,               # Juice 1,5L
    1817: ProductType.SPIRITS,             # Gin
    1819: ProductType.BREAD,               # FredagsFranskbrød
    1820: ProductType.BEER,                # Fadøl(Jul) i personligt glas
    1821: ProductType.SODA,                # 24 x 0,5 L sodavand uden pant
    1822: ProductType.BEER,                # Corona Extra & Franziskaner Dunk
    1823: ProductType.WATER,               # Budget kildevand incl. pant
    1824: ProductType.TICKET,              # F-dag
    1825: ProductType.BEER,                # Fadøl i kande (2 L)
    1826: ProductType.SNACK,               # Snack
    1827: ProductType.SERVICE,             # Konsulent for en aften
    1829: ProductType.BREAD,               # Brød
    1830: ProductType.TICKET,              # F-LAN
    1831: ProductType.CIDER_ALCOPOP,       # Cider/Garage
    1832: ProductType.SPIRITS,             # Alkohol (Snaps/shots)
    1833: ProductType.WATER,               # 1,5L vand excl. pant
    1834: ProductType.TICKET,              # Kamstrup Foobar
    1835: ProductType.MEAL,                # FLAN Sandwich lørdag frokost
    1836: ProductType.MEAL,                # FLAN Boller i karry Fredag aften
    1837: ProductType.ENERGY_DRINK,        # Monster
    1839: ProductType.WATER,               # Kurvand/Kildevand excl. pant
    1840: ProductType.BEER,                # Øl(Thy)
    1841: ProductType.TICKET,              # NetCompany Arrangement
    1842: ProductType.TICKET,              # Svedhytte
    1843: ProductType.UNKNOWN_BEVERAGE,    # Harbo 2 Liter
    1844: ProductType.BEER,                # Øl(Brewmaster)
    1845: ProductType.SODA,                # 1,5L sodavand
    1846: ProductType.BEER,                # Øl(Staropramen)
    1847: ProductType.BEER,                # Budweiser
    1848: ProductType.DEPOSIT,             # Pant A
    1849: ProductType.DEPOSIT,             # Pant C
    1850: ProductType.VITAMIN_WATER,       # Vitamin well
    1851: ProductType.SPORTS_PROTEIN_DRINK, # BCAA dåser - Lager salg
    1852: ProductType.TEA,                 # TE - Little Miracles
    1853: ProductType.BEER,                # Rød Tuborg - Maj Tilbud
    1854: ProductType.TICKET,              # Pop Up - Øl smagning
    1855: ProductType.BEER,                # Brooklyn
    1856: ProductType.BEER,                # Smithwik Pale Ale
    1857: ProductType.UNKNOWN_BEVERAGE,    # Harboe 0,5L
    1858: ProductType.BEER,                # Specialøl (3. hylde)
    1859: ProductType.BEER,                # Fyttetur Øl
    1860: ProductType.JUICE,               # Juice
    1861: ProductType.SPIRITS,             # Shots
    1862: ProductType.TICKET,              # Svedhytte
    1863: ProductType.JUICE,               # Ingefær shot lagersalg
    1864: ProductType.ENERGY_DRINK,        # AA Energi - Lagersalg
    1865: ProductType.COCOA,               # Lille cocio
    1866: ProductType.SNACK,               # Barbells- 3 stk
    1867: ProductType.SNACK,               # Barbells- 1 stk
    1868: ProductType.WATER,               # Stor vand (0,8L)
    1869: ProductType.CIDER_ALCOPOP,       # Somersby orchard selection
    1870: ProductType.SODA,                # 0.375L soda excl. pant (Mini)
    1871: ProductType.SNACK,               # Proteinbar - Barebells
    1872: ProductType.SPORTS_PROTEIN_DRINK, # Protein shake - Barebells
    1873: ProductType.VITAMIN_WATER,       # Vitamin Well - Fersken
    1874: ProductType.VITAMIN_WATER,       # Vitamin Well - Citron/Kaktus
}


def transform(data):
    data["member"] = transform_member(data["member"])
    data["location"] = transform_location(data["location"])
    products = transform_product(data["product"])
    data["product"] = prepare_product_changes(products, data["old_price"])
    data["sale"] = transform_sale(data)

    return data


def transform_sale(data):
    sale_data = data["sale"]

    # Filter out invalid sales based on member_id, room_id, and product_id
    valid_sale = (
        sale_data["member_id"].isin(data["member"]["id"])
        & sale_data["room_id"].isin(data["location"]["id"])
        & sale_data["product_id"].isin(data["product"]["item_id"])
    )
    filtered_data = sale_data.loc[valid_sale].copy() 

    timestamps = filtered_data["timestamp"].map(
        lambda timestamp: pd.to_datetime(
            timestamp,
            format="mixed",
            errors="coerce",
        )
    )
    filtered_data = filtered_data.loc[timestamps.notna()].copy()
    timestamps = timestamps.loc[filtered_data.index]
    target_timezone = timezone(timedelta(hours=1))
    timestamps = timestamps.map(
        lambda timestamp: (
            timestamp.tz_localize(target_timezone)
            if timestamp.tzinfo is None
            else timestamp.tz_convert(target_timezone)
        )
    )

    filtered_data["date_id"] = (
        timestamps.map(lambda timestamp: timestamp.year * 10000)
        + timestamps.map(lambda timestamp: timestamp.month * 100)
        + timestamps.map(lambda timestamp: timestamp.day)
    )
    filtered_data["time_id"] = (
        timestamps.map(lambda timestamp: timestamp.hour * 60)
        + timestamps.map(lambda timestamp: timestamp.minute)
    )

    return filtered_data.drop(columns=["timestamp"])

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
    product_data = product_data[["id", "name", "price", "alcohol_content_ml"]].copy()

    missing_ids = set(product_data["id"]) - PRODUCT_TYPE.keys()
    if missing_ids:
        raise ValueError(f"Products without a type: {sorted(missing_ids)}")

    missing_types = set(ProductType) - TYPE_CATEGORY.keys()
    if missing_types:
        names = sorted(product_type.value for product_type in missing_types)
        raise ValueError(f"Product types without a category: {names}")

    missing_categories = set(Category) - CATEGORY_CONSUMABLE.keys()
    if missing_categories:
        names = sorted(category.value for category in missing_categories)
        raise ValueError(f"Categories without a consumable mapping: {names}")

    # Map product to its type based on its id
    product_data["type"] = product_data["id"].map(
        {product_id: product_type.value for product_id, product_type in PRODUCT_TYPE.items()}
    )

    # Map product to its category based on its id
    product_data["category"] = product_data["id"].map(
        {
            product_id: TYPE_CATEGORY[product_type].value
            for product_id, product_type in PRODUCT_TYPE.items()
        }
    )

    # Set consumable for a product based on its category
    product_data["consumable"] = product_data["category"].map(
        {category.value: consumable for category, consumable in CATEGORY_CONSUMABLE.items()}
    )

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

    # Map alcohol_content_ml > 0 to contains_alcohol = true
    product_data["contains_alcohol"] = product_data["alcohol_content_ml"] > 0
    unknown_alcohol_content = product_data["alcohol_content_ml"].isna()
    if unknown_alcohol_content.any():
        names = product_data.loc[unknown_alcohol_content, "name"].unique().tolist()
        raise ValueError(f"Products with unknown alcohol content: {names}")

    return product_data


def prepare_product_changes(products, old_prices):
    history = old_prices[["product_id", "price", "changed_on"]].copy()
    excluded_product_ids = {1765, 1766}
    history = history.loc[~history["product_id"].isin(excluded_product_ids)]

    if history.isna().any().any():
        raise ValueError("Price history contains missing product IDs, prices, or timestamps")

    history["changed_on"] = pd.to_datetime(
        history["changed_on"], format="mixed", utc=True
    )

    # Fail if some price history references non-existing products
    missing_products = set(history["product_id"]) - set(products["id"])
    if missing_products:
        raise ValueError(f"Price history references missing products: {sorted(missing_products)}")

    # Drop duplicates
    history = history.drop_duplicates()

    conflicting = history.duplicated(["product_id", "changed_on"], keep=False)
    if conflicting.any():
        ids = sorted(history.loc[conflicting, "product_id"].unique().tolist())
        raise ValueError(f"Products with conflicting prices at the same timestamp: {ids}")

    history = history.sort_values(["product_id", "changed_on"])

    history_by_product = {
        product_id: rows.to_dict("records")
        for product_id, rows in history.groupby("product_id")
    }

    product_changes = []

    for product in products.to_dict("records"):
        changes = history_by_product.get(product["id"], [])

        if not changes:
            product_changes.append({
                **product,
                "changed_on": None,
            })
            continue

        for change in changes:
            product_changes.append({
                **product,
                "price": change["price"],
                "changed_on": change["changed_on"],
            })

    columns = [*products.columns, "changed_on"]
    return pd.DataFrame(product_changes, columns=columns).rename(columns={"id": "item_id"})


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
