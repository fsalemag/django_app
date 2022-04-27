.PHONY: up create down shell dump load
shell:
	docker-compose run web sh -c /bin/sh

create:
	docker-compose run web django-admin startproject website .

up:
	docker-compose up -d

down: 
	docker-compose down


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
