SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
PROJECT=fastapi_fast_start
OS = $(shell uname -s)
TAG    := $$(git describe --tags --always --abbrev=12)
IMG    := ${PROJECT}:${TAG}
LATEST := ${PROJECT}:latest

# Print usage of main targets when user types "make" or "make help"

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

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

compose-start-alembic: ## Start Alembic 
	(\
	clear; \
	echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo " Start Alembic creations and environment"; \
	echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	docker-compose -f docker-compose.yml down -v; \
	docker-compose -f docker-compose.yml up; \
	docker-compose exec web alembic init alembic; \
	)
.PHONY: compose-start-alembic

compose-migrations: ## Make migrations inside docker container
	( \
		echo " Remember to edit migrations config"; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Apllying migrations in containerized environment"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		docker-compose exec web alembic upgrade head; \
		echo "Show containers logs"; \
		docker-compose logs web; \
	)
.PHONY: compose-migrations

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

heroku: ## Deploy application to heroku
	(
		clear; \
		echo "Deploy heroku app"; \
		git subtree push --prefix app heroku master:main \
	)
.PHONY: heroku

build-tag:
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " Building containers and tag latest... "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "build docker tag '$(VERSION)'"; \
		docker-compose -f docker-compose.yml \
		build --parallel
		docker tag ${PROJECT} ${IMG} \
	)
.PHONY: build-tag