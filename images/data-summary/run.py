#!/usr/bin/env python

import sqlalchemy
import json

engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData(engine)
sqlalchemy.MetaData.reflect(metadata)

with open('sql/insert.sql', 'r') as sql:
  query = sql.read()

  statements = [
      statement for statement in query.split(";") if statement.strip() != ""
      ]
  for statement in statements:
      print(statement)
      connection.execute(statement)

# make an ORM object to refer to the table
CountrySummary = sqlalchemy.schema.Table('country_summary', metadata, autoload=True, autoload_with=engine)

# output the table to a JSON file
with open('/data/sample_output.json', 'w') as json_file:
  rows = connection.execute(sqlalchemy.sql.select([CountrySummary])).fetchall()
  rows = {row[0]: row[1] for row in rows}
  json.dump(rows, json_file, separators=(',', ':'))