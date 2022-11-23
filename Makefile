init-database:
	docker-compose up -d database
run-data-ingestion:
	docker-compose run data-ingestion
run-data-summary:
	docker-compose run data-summary