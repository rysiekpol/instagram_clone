#!/bin/bash
source venv/bin/activate
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - instagram:app