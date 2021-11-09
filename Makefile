# gets the environment variables in the .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# creates the database server and runs the pipeline
all: create_db run

# creates the database server
db_create: .tmp/db_create

# stops the database server
db_stop: .tmp/db_stop

# acccesses the database
# creates the databsae server if it is down
db: db_create
	@until [ "`docker inspect -f {{.State.Running}} postgres`"=="true" ]; do sleep 1; done 
	@PGPASSWORD=${POSTGRES_PASSWORD} psql -h localhost -p 5432 -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"

# runs the pipeline
#	scraps the data from the website
#	cleans the data
#	loads the data into the database
.PHONY: run
run:
	# TODO
	python3 -m pri-proj

# starts the docker container that holds the databse
.tmp/db_create:
	docker-compose build
	docker-compose -p pri up -d
	@mkdir -p .tmp
	@touch .tmp/db_create

# stops the database server
.tmp/db_stop:
	docker-compose -p pri stop
	@rm .tmp/db_create