#!/bin/bash
ping
gunicorn -b :5000 --timeout 300 --reload --access-logfile - --error-logfile - wsgi:app