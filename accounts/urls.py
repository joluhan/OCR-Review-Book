# Import the path function from django.urls to define url patterns
from django.urls import path
# Import the view functions from the current application's views module
from .views import login_page, signup_page
# Import LoginView and LogoutView from django.contrib.auth.views for authentication
from django.contrib.auth.views import LoginView, LogoutView

# List of URL patterns for the application
urlpatterns = [
    # Defines the URL pattern for the login page
    # Initially commented out is an alternative way to handle login using Django's built-in LoginView
    # path('', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    # The current login path uses a custom view named login_page for the root URL
    path('', login_page, name='login'),
    
    # Defines the URL pattern for the signup page
    # It uses a custom view named signup_page, accessible at '/signup/'
    path('signup/', signup_page, name='signup'),
    
    # Defines the URL pattern for the logout functionality
    # Uses Django's built-in LogoutView, accessible at '/logout/'
    # LogoutView.as_view() is used to create a class-based view instance on the fly
    path('logout/', LogoutView.as_view(), name='logout'),
]
