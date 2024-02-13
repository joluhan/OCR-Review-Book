# Import necessary Django modules and functions
from django.conf import settings  # Access project settings
from django.shortcuts import redirect, render  # Render templates and redirect users
from django.contrib.auth import login, authenticate  # Handle user authentication
from .forms import LoginForm, SignUpForm  # Import forms for login and signup
from django.views.generic import View  # Base class for creating class-based views

# Define a view for handling user sign-up
def signup_page(request):
    # Initialize a blank signup form
    form = SignUpForm()
    
    # Check if the request is a POST request, indicating form submission
    if request.method == 'POST':
        # Populate the form with data from the request
        form = SignUpForm(request.POST)
        
        # Validate the form data
        if form.is_valid():
            # Save the new user to the database
            user = form.save()
            
            # Log the user in (create a user session)
            login(request, user)
            
            # Redirect the user to a specified URL after successful signup
            return redirect(settings.LOGIN_REDIRECT_URL)
    
    # Render the signup template with the signup form
    return render(request, 'auth/signup.html', context={'form': form})

# Define a view for handling user login
def login_page(request):
    # Initialize a blank login form
    form = LoginForm()
    # Initialize an empty message for displaying login errors
    message = ''
    
    # Check if the request is a POST request, indicating form submission
    if request.method == 'POST':
        # Populate the form with data from the request
        form = LoginForm(request.POST)
        
        # Validate the form data
        if form.is_valid():
            # Attempt to authenticate the user with the provided credentials
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            # Check if authentication was successful
            if user is not None:
                # Log the user in (create a user session)
                login(request, user)
                
                # Redirect the user to the main feed after successful login
                return redirect('feed')
            else:
                # Update the message if credentials are invalid
                message = 'Invalid credentials'
    
    # Render the login template with the login form and message
    return render(request, 'auth/login.html', context={'form': form, 'message': message})

# Define a class-based view for handling user login
class LoginPage(View):
    # Specify the template name to be used
    template_name = 'auth/login.html'
    # Specify the form class to be used
    form_class = LoginForm

    # Handle GET requests - display the login form
    def get(self, request):
        # Initialize the form
        form = self.form_class()
        # Initialize an empty message for displaying login errors
        message = ''
        # Render the login template with the form and message
        return render(request, self.template_name, context={'form': form, 'message': message})

    # Handle POST requests - process the login form submission
    def post(self, request):
        # Populate the form with data from the request
        form = self.form_class(request.POST)
        # Initialize an empty message for displaying login errors
        message = ''
        
        # Validate the form data
        if form.is_valid():
            # Attempt to authenticate the user with the provided credentials
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            # Check if authentication was successful
            if user is not None:
                # Log the user in (create a user session)
                login(request, user)
                
                # Redirect the user to the home page after successful login
                return redirect('home')
            else:
                # Update the message if credentials are invalid
                message = 'Invalid credentials'
        
        # Render the login template with the form and message if login fails
        return render(request, self.template_name, context={'form': form, 'message': message})
