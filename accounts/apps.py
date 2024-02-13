# Import AppConfig class from django.apps module
from django.apps import AppConfig

# Define the configuration for the 'accounts' app
class AccountsConfig(AppConfig):
    # Specify the default auto field type for models in this app
    # Django uses this for primary keys if not overridden in model fields
    # 'django.db.models.BigAutoField' is a 64-bit integer, auto-incrementing primary key
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name attribute represents the full Python path to the application
    # It's used by Django to identify the app within the project
    # This should be the full Python path of the application
    name = 'accounts'
