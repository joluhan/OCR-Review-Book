# Import the admin module from django.contrib to customize the admin interface
from django.contrib import admin
# Import the User model from the current package's models module to register it with the admin site
from .models import User

# This class customizes how the User model is displayed in the Django admin interface
class UserAdmin(admin.ModelAdmin):
    # list_display is an attribute that specifies which fields should be displayed on the list page of the admin for this model
    list_display = ('username', 'email')  # Here, we choose to display the 'username' and 'email' fields

# Finally, we register the User model with the admin site, along with the UserAdmin class to customize its display
admin.site.register(User, UserAdmin)
