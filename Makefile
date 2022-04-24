.PHONY: up create down
create:
	docker-compose run web django-admin startproject django_project .

up:
	docker-compose up

down: docker-compose down
