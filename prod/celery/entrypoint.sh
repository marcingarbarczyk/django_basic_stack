#!/bin/bash

celery --app=accounts worker --loglevel=INFO -E -n worker@%h