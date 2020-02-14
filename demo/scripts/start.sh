#!/bin/bash

# Start Gunicorn processes
python /demo/manage.py runserver 0.0.0.0:8000 --insecure