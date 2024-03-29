#!/bin/bash
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - instagram:app
