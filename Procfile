release: python manage.py migrate && python manage.py compress
web: gunicorn ecommerce.wsgi --max-requests 1200 --timeout 300