from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from . forms import LoginForm, SignUpForm
from django.views.generic import View

# Create your views here.
def signup_page(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'auth/signup.html', context={'form': form})


# Create your views here.
def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                message = 'Invalid credentials'
    return render(request, 'auth/login.html', context={'form': form, 'message': message})


class LoginPage(View):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Invalid credentials'
        return render(request, self.template_name, context={'form': form, 'message': message})

