
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoaware_ph.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'staff_test'
password = 'password123'
email = 'staff@example.com'

try:
    user = User.objects.get(username=username)
    print(f"User {username} already exists.")
except User.DoesNotExist:
    user = User.objects.create_user(username=username, email=email, password=password)
    print(f"Created user {username}.")

# Make staff
if not user.is_staff:
    user.is_staff = True
    user.save()
    print(f"User {username} promoted to staff.")
else:
    print(f"User {username} is already staff.")
