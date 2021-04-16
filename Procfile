release: pipenv install
release: pipenv shell
release: python manage.py migrate
release: python manage.py fill
web: gunicorn ocpurbeurre.wsgi
