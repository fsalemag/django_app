# DOCKER
.PHONY: up down shell dump load build
shell:
	docker-compose run web sh -c /bin/bash

build:
	docker-compose build \
		--build-arg USER_ID=$(shell id -u $(USER)) \
		--build-arg GROUP_ID=$(shell id -g $(USER)) \
		--build-arg USER_NAME=app \
		--build-arg GROUP_NAME=app

up:
	docker-compose up

down: 
	docker-compose down


# DJANGO
.PHONY: create
create:
	docker-compose run web django-admin startproject website .


# DB
DUMP_FILE ?= dump.json
dump:
	docker-compose run web python manage.py dumpdata \
		--natural-foreign --natural-primary \
		-e contenttypes \
		-e auth.Permission \
		-e admin.logentry \
		-e sessions.session \
		-e auth.user \
		--indent 2 > $(DUMP_FILE)


load:
	docker-compose run web python manage.py loaddata $(DUMP_FILE)
