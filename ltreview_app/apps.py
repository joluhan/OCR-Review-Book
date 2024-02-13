# Import AppConfig from django.apps module to use it as a base class for your app's configuration.
from django.apps import AppConfig

# Define LtreviewConfig class which inherits from AppConfig.
# This class serves as the configuration class for your Django app named 'ltreview_app'.
class LtreviewConfig(AppConfig):
    # Specify the default auto field type for models in this app.
    # Django uses this field type when adding an automatic primary key field to your models.
    # 'django.db.models.BigAutoField' is used for primary keys that need a bigger range than what is offered by the standard AutoField.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name attribute is used to specify the full Python path to your application.
    # Django uses this configuration to locate and register the app within the project.
    # 'ltreview_app' is the custom name given to this Django application.
    name = 'ltreview_app'
