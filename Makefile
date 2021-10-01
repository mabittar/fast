SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
PROJECT=FastAPI_starer
OS = $(shell uname -s)


# Print usage of main targets when user types "make" or "make help"

help:
		"Please choose one of the following targets:"
	    "    setup: Setup your development environment and install dependencies"
	    "    run: Run app"
		"	 reload: Run app using reload mode"
		"	 lint: Lint file"
	    "    compose: Activate docker compose"
	    "    compose-up: Docker-up"
	    "    compose-down: Docker-down"
	    "    migrate: Make Alembic Migrations"
	    "    compose-build: Docker build App Image"
	    ""
	    "View the Makefile for more documentation about all of the available commands";
	@exit 2
.PHONY: help


setup: venv requirements-dev.txt
	(\
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Start LOCAL environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Check if virtual environment exists or initiate"; \
		if [ -d ./venv ]; \
		then \
		echo "virtual environment already exists skip initiation"; \
		else \
		echo "virtual environment does not exist start creation" \
		python -m venv venv; \
		fi; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Start virtual environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		source venv/bin/activate; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Install requirements-dev"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		pip install -r ./app/requirements-dev.txt; \
	)
.PHONY: setup

run:
	( \
		source venv/bin/activate; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Runinng APP"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. app/app.sh; \
	)
.PHONY: run

reload:
	( \
		source venv/bin/activate; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Runinng APP"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. app/app_reload.sh --reload; \
	)
.PHONY: reload

lint:
	( \
		source venv/bin/activate; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Linting APP"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		black --check .; \
		isort --recursive  --force-single-line-imports --line-width 88 --apply .; \
	)
.PHONY: lint

compose:
	( \
	clear; \
	echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo " Starting containerized environment"; \
	echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	docker-compose -f docker-compose.yml up; \
	docker-compose exec web alembic init -t async migrations; \
	)
.PHONY: compose

compose-up: 
	( \
	clear ; \
	docker-compose -f docker-compose.yml up --build; \
	)
.PHONY: compose-up

compose-down: 
	( \
		clear; \
		docker-compose -f docker-compose.yml down -v; \
	)
.PHONY: compose-down

migrations: 
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Apllying migrations in containerized environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		docker-compose exec web alembic upgrade head; \
		echo "Show containers logs"; \
		docker-compose logs web; \
	)
.PHONY: migrations

migrate: 
	( \
		clear; \
		echo "3 steps: Frist it'll bring down, then rebuild and after make migrations"; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " 1. Stop containerized environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		docker-compose -f docker-compose.yml down -v; \
		clear; \
		echo "3 steps: Frist it'll bring down, then rebuild and after make migrations"; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " 2. Start containerized environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		docker-compose -f docker-compose.yml up -d --build; \
		clear; \
		echo "3 steps: Frist it'll bring down, then rebuild and after make migrations"; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " 3. Apllying migrations in containerized environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		docker-compose exec web alembic init -t async migrations; \
		echo "Show containers logs"; \
		docker-compose logs web; \
	
	)
.PHONY: migrate

build:
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Building containers... "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		out/image-id: $(shell find app -type f)
		image_id="fastapi:$$(pwgen -1)"
		docker-compose -f docker-compose.yml \
		build --parallel \
		--build-arg \
		--tag="$${image_id}" \
		echo "$${image_id}" out/image-id; \
	)
.PHONY: build

