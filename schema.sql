DO $$
BEGIN
    CREATE TYPE gender_type AS ENUM ('Male', 'Female', 'Unknown');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    CREATE TYPE period_type AS ENUM ('sping_semester', 'fall_semester', 'summer_break', 'exam_period');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS member (
    member_id INTEGER PRIMARY KEY,
    signup_year INTEGER NOT NULL,
    gender gender_type NOT NULL
);

CREATE TABLE IF NOT EXISTS time (
    time_id INTEGER PRIMARY KEY,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    on_break BOOLEAN NOT NULL,
    schedule_slot INTEGER CHECK (schedule_slot BETWEEN 1 AND 4)
);

CREATE TABLE IF NOT EXISTS date (
    date_id INTEGER PRIMARY KEY,
    day INTEGER NOT NULL,
    month TEXT NOT NULL,
    year INTEGER NOT NULL,
    period period_type NOT NULL,
    working_day BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS location (
    place_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    is_event BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS product (
    item_version_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    volume INTEGER,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    consumable BOOLEAN NOT NULL,
    contains_alcohol BOOLEAN NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    valid_from TIMESTAMPTZ,
    valid_to TIMESTAMPTZ,
    CHECK (valid_from < valid_to)
);

CREATE TABLE IF NOT EXISTS sale (
    member_id INTEGER REFERENCES member(member_id),
    date_id INTEGER REFERENCES date(date_id),
    time_id INTEGER REFERENCES time(time_id),
    location_id INTEGER REFERENCES location(place_id),
    item_version_id INTEGER REFERENCES product(item_version_id),
    total_price NUMERIC(10, 2) NOT NULL,

    PRIMARY KEY (member_id, date_id, time_id, location_id, item_version_id)
);
