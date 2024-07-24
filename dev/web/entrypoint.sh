#!/bin/bash
echo "set enable-bracketed-paste off" >> ~/.inputrc # fix for multiple statements in python shell
python manage.py migrate
python manage.py runserver 0.0.0.0:80