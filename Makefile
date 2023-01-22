SHELL := /bin/bash

install:
	poetry install

run:
	poetry run python src/bug_manager/manage.py runserver

lint:
	find . -name '*.py' | xargs poetry run flake8

test:
	cd src/bug_manager && poetry run python manage.py test

migrate:
	poetry run python src/bug_manager/manage.py migrate

make-migrations:
	poetry run python src/bug_manager/manage.py makemigrations

build:
	docker build -t ticketmanager:latest . --build-arg SECRET_KEY="${SECRET_KEY}"

up:
	docker-compose up --build

up-detached:
	docker-compose up -d --build

down:
	docker-compose down

check-dependencies:
	poetry run dependency-check --scan . --out reports/ --failOnCVSS 7
