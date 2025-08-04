#!/bin/sh

set -e

echo "Applying database migrations..."
.venv/bin/python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Checking for superuser..."
.venv/bin/python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$DJANGO_SUPERUSER_USERNAME'
email = '$DJANGO_SUPERUSER_EMAIL'
password = '$DJANGO_SUPERUSER_PASSWORD'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
EOF

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf