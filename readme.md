# Fast API starter
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A multiple purpose Async project start using FastAPI

'A chef always sharpens his own knives'

## How to use
0. make sure pyenv is configured in your system
1. clone this repo
2. type make setup - It will update pyenv, check python version, create virtual environment and install dependencies
4. In dev environment use make reload to startup your API and reloads after changes
4.1 in live environment use make run - It will start up the API and server on localhost:8000.
5. you could start debug mode using vscode launch (press F5).
6. configure your database and local.env as you need
6. start develop your API


# Structure

## Root
env_config.py is the fle to load environment variables and configure your api
main.py file where API starts
requirements
makefile
docker files and docker yml


## Fast_api_load
Where API will be created and all resources like session to database, middleware and endpoints will be loaded

## Connectors
All outsource resources stay here, for example there is connector to external WeatherAPI

## Infrastructure
Resources like database connections and cache configuration

## Models
Represents database tables, schemas for requests and response

## Routers
Endpoints with requests validations, and response format

## Service
All logic, and access point to CRUD services

## Static
All statics files handle by API

## Template
HTML templates

## Utils
Utils files like, logger, rest connectors...




