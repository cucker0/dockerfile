#!/bin/bash
# Django create superuser

USER=admin
EMAIL=admin@example.com
PASSWORD=Dns123456!
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$USER', '$EMAIL', '$PASSWORD')" | python3 ./manage.py shell