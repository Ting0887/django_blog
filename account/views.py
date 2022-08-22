from email import message
from functools import reduce
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls.base import reverse
from account.forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'userForm':UserForm()})
    
    userForm = UserForm(request.POST)
    if not userForm.is_valid():
        return render(request, 'register.html', {'userForm':userForm})
    
    userForm.save()
    messages.success(request, '歡迎註冊帳號')
    return redirect('/account/login/')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'nextURL':request.GET.get('next')})
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.error(request, '請輸入資料')
        return render(request, 'login.html')
    
    user = authenticate(username=username, password=password)
    if not user:
        messages.error(request, '登入失敗，請再輸入一次')
        return render(request, 'login.html')
    
    auth_login(request, user)
    nextURL = request.POST.get('nextURL')
    if nextURL:
        return redirect(nextURL)
    messages.success(request, '登入成功')
    return redirect('/article/')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, '已登出帳號')
    return redirect('/account/login/')

def admin_required(func):
    def auth(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, '請以管理員身分登入')
            return redirect(reverse('account:login') +  '?next=' + request.get_full_path())
        return func(request, *args, **kwargs)
    return auth
