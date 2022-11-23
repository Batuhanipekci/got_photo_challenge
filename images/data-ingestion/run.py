#!/usr/bin/env python

import csv
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

from validations import validate_date, format_text
# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
try:
    connection = engine.connect()
    print("Connected to the database with success")
except SQLAlchemyError as err:
    print("Database Connection Error", err.__cause__)

metadata = sqlalchemy.schema.MetaData(engine)
sqlalchemy.MetaData.reflect(metadata)

# make ORM objects to refer to the tables
City = metadata.tables['city']
County = metadata.tables['county']
Country = metadata.tables['country']
Person = metadata.tables['person']

#City = sqlalchemy.schema.Table('city', metadata, autoload=True, autoload_with=engine)
#County = sqlalchemy.schema.Table('county', metadata, autoload=True, autoload_with=engine)
#Country = sqlalchemy.schema.Table('country', metadata, autoload=True, autoload_with=engine)
#Person = sqlalchemy.schema.Table('person', metadata, autoload=True, autoload_with=engine)


def update_if_not_exists(connection, orm_object, feature_dict):
  value = connection.execute(
    sqlalchemy.select(orm_object).filter_by(**feature_dict)
    ).all()
  if len(value)==0:
    pk = connection.execute(orm_object.insert().values(**feature_dict)).inserted_primary_key[0]
    print(pk)
    return pk
  pk = value[0][0]
  return pk

# read the places CSV data file into the respective tables
with open('/data/places.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  for row in reader:
    city_name = format_text(row[0])
    county_name = format_text(row[1])
    country_name = format_text(row[2])

    country_id = update_if_not_exists(connection, Country, {'name':country_name})
    county_id = update_if_not_exists(connection, County, {'name':county_name, 'country_id':country_id})
    city_id = update_if_not_exists(connection, City, {'name':city_name, 'county_id':county_id})

with open('/data/people.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  for row in reader:
    given_name = format_text(row[0])
    family_name = format_text(row[1])
    date_of_birth = validate_date(row[2])
    city_name = format_text(row[3])

    city_id = update_if_not_exists(connection, City, {'name':city_name})
    person_result = update_if_not_exists(connection, Person, {
      
      'given_name':given_name,
      'family_name':family_name,
      'date_of_birth':date_of_birth,
      'city_id':city_id
      })
