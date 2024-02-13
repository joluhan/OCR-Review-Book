# Import necessary modules and functions for URL configuration
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

# urlpatterns: A list of URL patterns for routing URLs to their corresponding views.
urlpatterns = [
    # Admin site URLs.
    # This pattern routes the URL ending with 'admin/' to Django's admin interface.
    path('admin/', admin.site.urls),
    
    # Include accounts app URLs.
    # This includes the URL patterns from the 'accounts' app, allowing the project to delegate
    # URL handling for anything related to user accounts to the accounts app.
    path('', include('accounts.urls')),
    
    # Include ltreview_app app URLs.
    # This includes the URL patterns from the 'ltreview_app', routing URLs for the main features
    # of the LITReview project to the respective views in the ltreview_app application.
    path('', include('ltreview_app.urls')),
]

# Serve static files in development
# This conditional addition uses Django's static file serving mechanism for development purposes.
# It serves static files (CSS, JavaScript, images) located under STATIC_URL during development.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
# Similar to static files, this routes media file URLs (uploaded by users) to be served
# from MEDIA_ROOT during development, making it possible to access user-uploaded content.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
