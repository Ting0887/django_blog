from django.shortcuts import redirect, render, get_object_or_404
from myblog.forms import LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout as auth_logout

# Create your views here.

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            print('not found')
            user = auth.authenticate(username=user.username, password=password)
            if user is not None and user.is_active or user.is_superuser:
                auth.login(request, user)
                return redirect('/home/')

    return render(request, "account/login.html", {'form': form})

@login_required(login_url='Login')
def logout(request):
    auth_logout(request) 
    return redirect('/login/')    