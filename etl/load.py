from datetime import date, timedelta
from enum import Enum
from pygrametl.tables import CachedDimension
from db import connect


class Period(str, Enum):
    SPRING_SEMESTER = "sping_semester"
    FALL_SEMESTER = "fall_semester"
    SUMMER_BREAK = "summer_break"
    EXAM_PERIOD = "exam_period"


def load(transformed_data):
    connection = connect()
    try:
        load_member_dimension(connection, transformed_data["member"])
        prefill_date_dimension(connection)
        prefill_time_dimension(connection)

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return transformed_data

def load_member_dimension(connection, member_data):
    
    member_dimension = CachedDimension(
        name="member",
        key="member_id",
        attributes=["signup_year", "gender"],
        lookupatts=["member_id"],
        targetconnection=connection
    )

    for row in member_data.to_dict("records"):
        member_dimension.ensure({
            "member_id": row["id"],
            "signup_year": row["year"],
            "gender": row["gender"]
        })

def prefill_date_dimension(connection):
    date_dimension_data = generate_date_data(date(1976, 1, 1), date.today())

    date_dimension = CachedDimension(
        name="date",
        key="date_id",
        attributes=["day", "month", "year", "period", "working_day"],
        lookupatts=["year", "month", "day"],
        targetconnection=connection
    )

    for row in date_dimension_data:
        date_dimension.ensure({
            "date_id": row['year']*10000 + row['month']*100 + row['day'],
            "day": row["day"],
            "month": row["month"],
            "year": row["year"],
            "period": row["period"],
            "working_day": row["working_day"]
        })

def prefill_time_dimension(connection):
    time_dimension_data = generate_time_data()

    time_dimension = CachedDimension(
        name="time",
        key="time_id",
        attributes=["minute", "hour", "on_break", "schedule_slot"],
        lookupatts=["hour", "minute"],
        targetconnection=connection
    )

    for row in time_dimension_data:
        time_dimension.ensure({
            "time_id": row['hour']*60 + row['minute'],
            "minute": row["minute"],
            "hour": row["hour"],
            "on_break": row["on_break"],
            "schedule_slot": row["schedule_slot"]
        })

def generate_date_data(start_date, end_date):
    dates = []

    current = start_date

    while current <= end_date:
        dates.append({
            "day": current.day,
            "month": current.month,
            "year": current.year,
            "period": period(current.month),
            "working_day": current.weekday() < 5 and not holidays(current)
        })

        current += timedelta(days=1)

    return dates

def generate_time_data():
    times = []

    for minute in range(1440):
        hour = minute // 60

        times.append({
            "minute": minute,
            "hour": hour,
            "on_break": on_break(hour, minute),
            "schedule_slot": schedule_slot(hour, minute)
        })

    return times    

def period(month):
    if month in (2, 3, 4, 5):
        return Period.SPRING_SEMESTER.value
    elif month in (7, 8):
        return Period.SUMMER_BREAK.value
    elif month in (9, 10, 11, 12):
        return Period.FALL_SEMESTER.value
    else:
        return Period.EXAM_PERIOD.value
    
def on_break(hour, minute):
    current_minute = hour * 60 + minute
    return any(
        current_minute in break_period
        for break_period in (
            range(10 * 60 + 1, 10 * 60 + 15),
            range(12 * 60 + 1, 12 * 60 + 30),
            range(14 * 60 + 16, 14 * 60 + 30),
        )
    )

def schedule_slot(hour, minute):
    current_minute = hour * 60 + minute
    slots = (
        (8 * 60 + 15, 10 * 60, 1),
        (10 * 60 + 15, 12 * 60, 2),
        (12 * 60 + 30, 14 * 60 + 15, 3),
        (14 * 60 + 30, 16 * 60 + 15, 4),
    )

    for start, end, slot in slots:
        if start <= current_minute <= end:
            return slot
        
    return None

def holidays(day):
    """Return whether day is a Danish public holiday."""
    easter_sunday = calculate_easter_sunday(day.year)

    holidays = ({
        date(day.year, 1, 1),                # nytårsdag
        easter_sunday - timedelta(days=3),   # skærtorsdag
        easter_sunday - timedelta(days=2),   # langfredag
        easter_sunday,                       # påskedag
        easter_sunday + timedelta(days=1),   # 2. påskedag
        easter_sunday + timedelta(days=39),  # kristihimmelfartsdag
        easter_sunday + timedelta(days=49),  # pinsedag
        easter_sunday + timedelta(days=50),  # 2. pinsedag
    }| {date(day.year, 12, day_of_month) for day_of_month in range(24, 32)} #juleferie
    )| {date(day.year, month, day_of_month) for day_of_month in range(1, 32) for month in (7,8)} #sommerferie

    # vi må ikke glemme store Bededag (RIP)
    if day.year <= 2023:
        holidays.add(easter_sunday + timedelta(days=26))

    return day in holidays


def calculate_easter_sunday(year):
    """Calculate Easter Sunday using the Gregorian computus algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year, month, day)
