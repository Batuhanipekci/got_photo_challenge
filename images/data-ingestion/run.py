#!/usr/bin/env python
"""
This module defines functionalities for ingesting csv files
to the database schema.
"""
import csv
import sqlalchemy
from validations import validate_date, format_text

# connect to the database
ENGINE = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
try:
    CONNECTION = ENGINE.connect()
    print("Connected to the database with success")
except sqlalchemy.exc.SQLAlchemyError as err:
    print("Database Connection Error", err.__cause__)

METADATA = sqlalchemy.schema.MetaData(ENGINE)
sqlalchemy.MetaData.reflect(METADATA)

# make ORM objects to refer to the tables
CITY = METADATA.tables["city"]
COUNTY = METADATA.tables["county"]
COUNTRY = METADATA.tables["country"]
PERSON = METADATA.tables["person"]


def update_if_not_exists(
        connection: sqlalchemy.engine.Engine,
        orm_object: sqlalchemy.Table,
        feature_dict: dict,
    ) -> str:
    """
    Queries a table in the database given a feature_dict,
        - if the entry exists, extracts the value list,
        - else inserts the value
        returns the primary key of the value.

    :param connection: database connector
    :type connection: sqlalchemy.engine.Engine
    :param orm_object: ORM Table object to query the database
    :type orm_object: sqlalchemy.Table
    :param feature_dict: value properties to unpack into the query.
    :type feature_dict: dict
    """
    value = connection.execute(
        sqlalchemy.select(orm_object).filter_by(**feature_dict)
    ).all()
    if not value:
        primary_key = connection.execute(
            orm_object.insert().values(**feature_dict)
        ).inserted_primary_key[0]
        return primary_key
    primary_key = value[0][0]
    return primary_key


# read the places CSV data file into the respective tables
print("Reading and importing places.csv")
with open("/data/places.csv") as csv_file:
    READER = csv.reader(csv_file)
    next(READER)
    for row in READER:
        print(f"row: {row}")
        city_name = format_text(row[0])
        county_name = format_text(row[1])
        country_name = format_text(row[2])

        country_id = update_if_not_exists(CONNECTION, COUNTRY, {"name": country_name})
        county_id = update_if_not_exists(
            CONNECTION, COUNTY, {"name": county_name, "country_id": country_id}
        )
        city_id = update_if_not_exists(
            CONNECTION, CITY, {"name": city_name, "county_id": county_id}
        )


# Read the people.csv into respective tables
print("Reading and importing people.csv")
with open("/data/people.csv") as csv_file:
    READER = csv.reader(csv_file)
    next(READER)
    for row in READER:
        print(f"row: {row}")
        given_name = format_text(row[0])
        family_name = format_text(row[1])
        date_of_birth = validate_date(row[2])
        city_name = format_text(row[3])

        city_id = update_if_not_exists(CONNECTION, CITY, {"name": city_name})
        person_result = update_if_not_exists(
            CONNECTION,
            PERSON,
            {
                "given_name": given_name,
                "family_name": family_name,
                "date_of_birth": date_of_birth,
                "city_id": city_id,
            },
        )
