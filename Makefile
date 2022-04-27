.PHONY: up create down
create:
	docker-compose run web django-admin startproject website .

up:
	docker-compose up -d

down: 
	docker-compose down
