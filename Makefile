# DOCKER
DOCKER_BUILD_ARGS := --build-arg USER_ID=$(shell id -u $(USER))
DOCKER_BUILD_ARGS += --build-arg GROUP_ID=$(shell id -g $(USER))
DOCKER_BUILD_ARGS += --build-arg USER_NAME=app
DOCKER_BUILD_ARGS += --build-arg GROUP_NAME=app

.PHONY: up down shell dump load build build-dev build-prod
shell:
	docker-compose run web sh -c /bin/bash

build-dev: build_dev
build-prod: build_prod
build_%:
		docker-compose -f $*.docker-compose.yml \
			build $(DOCKER_BUILD_ARGS) \

up-dev: up_dev
up-prod: up_prod
up_%:
	docker-compose -f $*.docker-compose.yml up

down-dev: down_dev
down-prod: down_prod
down_%:
	docker-compose -f $*.docker-compose.yml down


# DJANGO
.PHONY: create
create:
	docker-compose run web django-admin startproject website .


# DB
DUMP_FILE ?= dump.json
dump-dev: dump_dev
dump-prod: dump_prod
dump_%:
	docker-compose -f $*.docker-compose.yml run web python manage.py dumpdata \
		--natural-foreign --natural-primary \
		-e contenttypes \
		-e auth.Permission \
		-e admin.logentry \
		-e sessions.session \
		-e users \
		-e auth.user \
		--indent 2 > $(DUMP_FILE)


load-dev: load_dev
load-prod: load_prod
load_%:
	docker-compose -f $*.docker-compose.yml run web python manage.py loaddata $(DUMP_FILE)
