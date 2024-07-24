# Django Basic Stack

## Features:

* Dockerized
* All needed dependencies for modern web apps
* Pre commit with hooks
* Prepare for github actions
* Production and staging settings

## How to use:

1. Rename folder of this repo.
2. Rename all string from "django_basic_stack" to "your_app_name".
3. Rename all string from "DJANGO_BASIC_STACK" to "YOUR_APP_NAME".

## How to start:

1. Run "docker compose build web" in main repo's folder.
2. Run "docker compose up -d".
3. Optional: you can use command: "python manage.py create_initial_data" in your container.

## Additional info:

1. In Makefile you have some useful commands for example: compile_packages


## Soon

1. User extended
2. Elastic Search