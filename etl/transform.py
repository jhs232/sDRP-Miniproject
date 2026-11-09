from datetime import date

def transform(data):
    data["member"] = transform_member(data["member"])

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
