from django.urls import path
from .views import login_page, signup_page
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path('', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]