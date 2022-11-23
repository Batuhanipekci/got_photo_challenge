#!/usr/bin/env python

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import json

engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")

# connect to the database
try:
    connection = engine.connect()
    print("Connected to the database with success")
except SQLAlchemyError as err:
    print("Database Connection Error", err.__cause__)

metadata = sqlalchemy.schema.MetaData(engine)
sqlalchemy.MetaData.reflect(metadata)

# run prepared sql script to populate summary tables
with open("sql/insert.sql", "r") as sql:
    query = sql.read()

    statements = [
        statement for statement in query.split(";") if statement.strip() != ""
    ]
    for statement in statements:
        print(statement)
        connection.execute(statement)

# make an ORM object to refer to the table
CountrySummary = sqlalchemy.schema.Table(
    "country_summary", metadata, autoload=True, autoload_with=engine
)

# fetch the summary data from database and
# output the table to a JSON file
with open("/data/sample_output.json", "w") as json_file:
    rows = connection.execute(sqlalchemy.sql.select([CountrySummary])).fetchall()
    rows = {row[0]: row[1] for row in rows}
    json.dump(rows, json_file, separators=(",", ":"))
