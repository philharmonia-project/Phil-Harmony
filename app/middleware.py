# Create a file: middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # If user just logged in and is on the Google callback page, redirect to home
        if (request.user.is_authenticated and 
            request.path == '/accounts/google/login/callback/'):
            return redirect('user_home')
            
        return response