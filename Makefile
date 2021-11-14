SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
PROJECT=FastAPI_starer
OS = $(shell uname -s)

.DEFAULT_GOAL := help

# Print usage of main targets when user types "make" or "make help"

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


setup: venv requirements-dev.txt ## Setup your development environment and install dependencies
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
		pip install -r ./requirements-dev.txt; \
	)
.PHONY: setup

run: ## Run app
	( \
		source venv/bin/activate; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Runinng APP"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. app/app.sh; \
	)
.PHONY: run

reload: ## Run app reload  mode
	( \
		source venv/bin/activate; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Runinng APP"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. app/app_reload.sh --reload; \
	)
.PHONY: reload

lint: ## Lint files and structure using pep8 and sortimports
	( \
		source venv/bin/activate; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Linting APP"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		black --check -l 120 -t py39 ./app; \
		isort --force-single-line-imports --line-width 120 --skip **/*__init__.py ./app; \
	)
.PHONY: lint

compose: ## Start docker
	( \
	clear; \
	echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo " Starting containerized environment"; \
	echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	docker-compose -f docker-compose.yml up; \
	docker-compose exec web alembic init -t async migrations; \
	)
.PHONY: compose

compose-up: ## Build docker using docker-compose.yml
	( \
	clear ; \
	docker-compose -f docker-compose.yml up --build; \
	)
.PHONY: compose-up

compose-down: ## Stop docker env
	( \
		clear; \
		docker-compose -f docker-compose.yml down -v; \
	)
.PHONY: compose-down

migrations: ## Make migrations inside docker container
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

migrate: ## Stop docker, and applying migrations in containerized environment
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
		out/image-id: $(shell find ./app -type f)
		image_id="fastapi:$$(pwgen -1)"
		docker-compose -f docker-compose.yml \
		build --parallel \
		--build-arg \
		--tag="$${image_id}" \
		echo "$${image_id}" out/image-id; \
	)
.PHONY: build