from datetime import date

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
