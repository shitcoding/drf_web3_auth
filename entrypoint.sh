#!/usr/bin/env sh
set -e

SERVICE=app
WORKERS=2
BIND=0.0.0.0:8000

cd /app && chown -R $SERVICE:$SERVICE ./

# Wait for postgres startup
python3 ./utils/wait_postgres.py

echo "---------------------------"
echo " Apply database migrations "
echo "---------------------------"
python manage.py migrate

echo "----------------------"
echo " Collect static files "
echo "----------------------"
python manage.py collectstatic --no-input


echo "----------------"
echo " Start gunicorn "
echo "----------------"
gunicorn core.wsgi -u $SERVICE -g $SERVICE -w $WORKERS -b $BIND
