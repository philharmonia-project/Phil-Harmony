# utils/setup_superuser.py
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import os

def setup_superuser(request):
    """
    Create a superuser using environment variables if none exists.
    This is meant to run once after deployment.
    """

    User = get_user_model()

    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Superuser already exists.")

    # Read environment variables
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

    if not username or not password or not email:
        return HttpResponse("Superuser environment variables are missing.", status=500)

    # Create superuser
    User.objects.create_superuser(username=username, email=email, password=password)

    return HttpResponse(f"Superuser '{username}' created successfully!")
