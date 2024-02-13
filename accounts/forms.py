# Import forms module from django to create form classes
from django import forms
# Import get_user_model function to get the current active user model
from django.contrib.auth import get_user_model
# Import UserCreationForm class to inherit for creating a user signup form
from django.contrib.auth.forms import UserCreationForm

# Define a form for the login process
class LoginForm(forms.Form):
    # Username field with a maximum length of 63 characters
    username = forms.CharField(max_length=63, label="Username")
    # Password field with a maximum length of 63 characters
    # PasswordInput widget is used here to render it as a password input field, hiding the typed characters
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Password')

# Define a form for the signup process by inheriting UserCreationForm
class SignUpForm(UserCreationForm):
    # Meta class to provide additional information about the SignUpForm class
    class Meta(UserCreationForm.Meta):
        # Specifying the model that this form is for (User model)
        # get_user_model() dynamically retrieves the custom or default user model
        model = get_user_model()
        # Fields to include in the form, in this case, only 'username'
        # It uses fields from the User model (or the custom user model if one is being used)
        fields = ['username']
