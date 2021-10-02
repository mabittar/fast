# Fast API starter
[![author](https://img.shields.io/badge/Author-MarcelBittar-blue)](https://www.linkedin.com/in/marcelbittar/)   [![](https://img.shields.io/badge/dependencies-pyenv-red.svg)](https://github.com/pyenv/pyenv) [![](https://img.shields.io/badge/python-3.9.2+-blue.svg)](https://www.python.org/downloads/release/python-392/)    [![](https://img.shields.io/badge/dependencies-FastAPI-yellow.svg)](https://fastapi.tiangolo.com/)     [![](https://img.shields.io/badge/dependencies-SQLModel-yellow.svg)](https://sqlmodel.tiangolo.com/)     [![](https://img.shields.io/badge/build-passing-green.svg)](https://sqlmodel.tiangolo.com/)[![](https://img.shields.io/badge/docker%20build-passing-green.svg)](https://sqlmodel.tiangolo.com/)   [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/mabittar/Portfolio/issues)

A multiple purpose Async project start using FastAPI

'A chef always sharpens his own knives'

## How to use
0. make sure pyenv is configured in your system
1. clone this repo

You could use make file to setup env and start API

2. type make setup - It will update pyenv, check python version, create virtual environment and install dependencies
4. In dev environment use make reload to startup your API and reloads after changes
4.1 in live environment use make run - It will start up the API and server on localhost:8000.
5. you could start debug mode using vscode launch (press F5).
6. at our browser go to http://127.0.0.1:8000
7. check interactive documentation on http://127.0.0.1:8000/docs


6. configure your database and .env as you need
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




