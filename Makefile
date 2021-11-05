# gets the environment variables in the .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# starts the docker container that holds the databse
create_db:
	docker-compose build
	docker-compose up

# acccesses the database
db:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5432 -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"

# runs the pipeline
#	scraps the data from the website
#	cleans the data
#	loads the data into the database
run:
	# TODO
	python3 -m pri-proj