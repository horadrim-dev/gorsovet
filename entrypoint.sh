#!/bin/sh

cd /app
#pip install -r requirements.txt
if [ "$DATABASE" = "postgres" ]
then
	echo "Waiting for postgres..."

	while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
	      sleep 0.1
	done

	echo "PostgreSQL started"
fi

# If called very early the curl will receive an "empty" response and a failing status
# As soon as Elasticsearch can process the command, it will return a success status
# as soon as the cluster is yellow or green
# echo "Waiting for es..."
# until curl $ELASTICSEARCH_HOST'/_cluster/health?wait_for_status=green&timeout=1s'; do
#   >&2 sleep 1
# done

# while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
# 		sleep 0.1
# done

echo "Elasticsearch started"

python manage.py migrate
python manage.py filer_check --delete-missing --noinput
rm -r ./staticfiles/CACHE/
python manage.py collectstatic --noinput
chmod 755 $(find ./staticfiles -type d)
chmod 755 $(find ./mediafiles -type d)
chmod 644 $(find ./staticfiles -type f)
chmod 644 $(find ./mediafiles -type f)
python manage.py rebuild_index --noinput

exec "$@"
