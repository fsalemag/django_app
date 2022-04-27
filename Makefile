.PHONY: up create down shell
create:
	docker-compose run web django-admin startproject website .

up:
	docker-compose up -d

down: 
	docker-compose down

shell:
	docker-compose run web bash -c /bin/bash