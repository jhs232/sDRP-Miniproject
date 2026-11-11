from datetime import date, timedelta, timezone
import pandas as pd


def transform(data):
    data["member"] = transform_member(data["member"])
    data["location"] = transform_location(data["location"])
    data["sale"] = transform_sale(data)

    return data


def transform_sale(data):
    sale_data = data["sale"]

    # Filter out invalid sales based on member_id, room_id, and product_id
    valid_sale = (
        sale_data["member_id"].isin(data["member"]["id"])
        & sale_data["room_id"].isin(data["location"]["id"])
        & sale_data["product_id"].isin(data["product"]["product_id"])
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
    
    member_data["gender"] = member_data["gender"].map({
        "M": "Male",
        "F": "Female",
        "U": "Unknown",
    })
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
