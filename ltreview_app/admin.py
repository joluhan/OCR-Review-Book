# Import the admin module from django.contrib to enable admin interface configurations.
from django.contrib import admin
# Import the Ticket and Review models from the current package's models module.
# These models represent the database structure for tickets and reviews respectively.
from .models import Ticket, Review

# Register the Ticket model with the admin site using admin.site.register() method.
# This makes the Ticket model accessible and manageable through the Django admin interface,
# allowing administrators to add, edit, delete, and view Ticket instances.
admin.site.register(Ticket)

# Register the Review model with the admin site using the same method as above.
# This action integrates the Review model into the Django admin,
# enabling admin users to perform CRUD operations on Review instances directly from the admin interface.
admin.site.register(Review)
