import csv
import json
from datetime import datetime

import sqlalchemy
from sqlalchemy import text


DATABASE_URL = (
    "mysql+mysqlconnector://"
    "user_dteng:cirilgroupt@127.0.0.1:3306/db_dteng"
)

engine = sqlalchemy.create_engine(DATABASE_URL)


def normalize_city(city):
    """Normalize a city name for consistent matching."""
    return " ".join(city.strip().split()).lower()


def is_missing(value):
    """Return True if a CSV value is empty or contains only whitespace."""
    return not value or not value.strip()


def valid_date(value):
    """Check that the date uses YYYY-MM-DD format."""
    try:
        datetime.strptime(value.strip(), "%Y-%m-%d")
        return True
    except (ValueError, AttributeError):
        return False


with engine.begin() as connection:

    ## Clear tables 

    connection.execute(text("DELETE FROM people"))
    connection.execute(text("DELETE FROM places"))
    
    # -------------------------
    # Load places.csv
    # -------------------------

    places = []

    with open("data/places.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            places.append({
                "city": normalize_city(row["city"]),
                "county": row["county"].strip(),
                "country": row["country"].strip(),
            })

    connection.execute(
        text("""
            INSERT INTO places (city, county, country)
            VALUES (:city, :county, :country)
        """),
        places
    )

    print(f"Loaded {len(places)} places")

    # -------------------------
    # Load people.csv
    # -------------------------

    people = []
    skipped_missing = 0
    skipped_invalid_date = 0

    with open("data/people.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            # Required fields
            if (
                is_missing(row["given_name"])
                or is_missing(row["family_name"])
                or is_missing(row["place_of_birth"])
            ):
                skipped_missing += 1
                continue

            # Date validation
            if not valid_date(row["date_of_birth"]):
                skipped_invalid_date += 1
                continue

            people.append({
                "given_name": row["given_name"].strip(),
                "family_name": row["family_name"].strip(),
                "date_of_birth": row["date_of_birth"].strip(),
                "place_of_birth": normalize_city(row["place_of_birth"]),
            })

    connection.execute(
        text("""
            INSERT INTO people
                (given_name, family_name, date_of_birth, place_of_birth)
            VALUES
                (:given_name, :family_name, :date_of_birth, :place_of_birth)
        """),
        people
    )

    print(f"Loaded {len(people)} people")
    print(f"Skipped {skipped_missing} people with missing required values")
    print(f"Skipped {skipped_invalid_date} people with invalid dates")

    # -------------------------
    # Export births by country
    # -------------------------

    result = connection.execute(
        text("""
            SELECT
                p.country,
                COUNT(*) AS births
            FROM people pe
            JOIN places p
                ON pe.place_of_birth = p.city
            GROUP BY p.country
            ORDER BY p.country
        """)
    )

    output = {
    row.country: row.births
    for row in result
    }

    with open("data/output.json", "w", encoding="utf-8") as file:
        json.dump(output, file, separators=(",", ":"))

    print("Exported data/output.json")