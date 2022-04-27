.PHONY: up create down shell
shell:
	docker-compose run web bash -c /bin/bash

create:
	docker-compose run web django-admin startproject website .

up:
	docker-compose up -d

down: 
	docker-compose down
