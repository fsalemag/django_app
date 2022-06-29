#!/bin/bash
ssh linode "cd django_app_staging && git stash && git checkout master && git pull && make down-stag && make up-stag"
