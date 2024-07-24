#!/bin/bash
PORT=${1:-8000}
echo "set enable-bracketed-paste off" >> ~/.inputrc # fix for multiple statements in python shell
mkdir -p /logs/django_basic_stack/gunicorn
python manage.py collectstatic --no-input --clear
python manage.py migrate
gunicorn -b 0.0.0.0:$PORT django_basic_stack.wsgi:application -w 1 -t 300 --preload --access-logfile /logs/django_basic_stack/gunicorn/access.log --capture-output --enable-stdio-inheritance --access-logformat '%({x-forwarded-for}i)s %(t)s %(l)s %(s)s "%(r)s" %(l)s %(a)s'
