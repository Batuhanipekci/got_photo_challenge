This repository orchestrates containers for database, data ingestion service, and data summary service.

Key features:
- Database is initialized via the schema.sql during the setup of the container. No volume is mounted for the database, it is ephemeral.
- data-ingestion image takes the csv files as input and populates the given schema of the database.
- data-summary image summarizes the master schema and populates summary tables using a sql script. Then it exports the summary data from database in JSON format.
- Unit test and data integrity test ideas have been sketched.

To run the program, please execute the following commmands in the given order:
```
	docker-compose up -d database
	docker-compose run data-ingestion
	docker-compose run data-summary
```
