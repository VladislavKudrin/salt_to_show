release: python manage.py migrate
web: gunicorn ecommerce.wsgi --max-requests 1200 --timeout 300