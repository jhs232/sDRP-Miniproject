CREATE TYPE gender_type AS ENUM ('Male', 'Female', 'Unknown');
CREATE TYPE period_type AS ENUM ('sping_semester', 'fall_semester', 'summer_break', 'exam_period');

CREATE TABLE IF NOT EXISTS member (
    member_id INTEGER PRIMARY KEY,
    signup_year INTEGER NOT NULL,
    gender gender_type NOT NULL
);

CREATE TABLE IF NOT EXISTS time (
    time_id SERIAL PRIMARY KEY,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    on_break BOOLEAN NOT NULL,
    schedule_slot INTEGER CHECK (schedule_slot BETWEEN 1 AND 4)
);

CREATE TABLE IF NOT EXISTS date (
    date_id SERIAL PRIMARY KEY,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    period period_type NOT NULL,
    working_day BOOLEAN NOT NULL
);