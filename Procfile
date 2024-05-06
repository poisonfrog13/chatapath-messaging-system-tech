release: echo "hello world"
release: python manage.py collectstatic
release: python manage.py migrate
web: gunicorn server.wsgi
