#!/bin/bash
ping
gunicorn -b :5000 -k gevent -w 1 --reload --timeout 300 --access-logfile - --error-logfile - wsgi:app