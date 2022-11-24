#!/usr/bin/env python
"""
This module defines functionalities for summarizing
data in the database and exporting the json output.
"""
import json
import sqlalchemy

ENGINE = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")

# connect to the database
try:
    CONNECTION = ENGINE.connect()
    print("Connected to the database with success")
except sqlalchemy.exc.SQLAlchemyError as err:
    print("Database Connection Error", err.__cause__)

METADATA = sqlalchemy.schema.MetaData(ENGINE)
sqlalchemy.MetaData.reflect(METADATA)

# run prepared sql script to populate summary tables
print("Reading the sql queries for summarizing data")
with open("sql/insert.sql", "r") as sql:
    QUERY = sql.read()

    STATEMENTS = [
        statement for statement in QUERY.split(";") if statement.strip() != ""
    ]
    for statement in STATEMENTS:
        CONNECTION.execute(statement)

# make an ORM object to refer to the table
COUNTRY_SUMMARY = sqlalchemy.schema.Table(
    "country_summary", METADATA, autoload=True, autoload_with=ENGINE
)

# fetch the summary data from database and
# output the table to a JSON file
print("Extracting summary data")
with open("/data/sample_output.json", "w") as json_file:
    DATA = CONNECTION.execute(sqlalchemy.sql.select([COUNTRY_SUMMARY])).fetchall()
    ROWS = {row[0]: row[1] for row in DATA}
    json.dump(ROWS, json_file, separators=(",", ":"))
print("Success in extracting summary data! You can find the output under data folder.")
