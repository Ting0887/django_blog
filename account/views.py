from ast import Return
from cProfile import Profile
from email import message
from functools import reduce
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.urls.base import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from account.forms import UserForm, ProfileForm, ForgetPasswordForm
from account.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings

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

def forgetPassword(request):
    form = ForgetPasswordForm()
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    mailto = user.email
                    mailsubject = 'Yukina的部落格 - 密碼重設通知'
                    mailcontent = f"""{ user.fullName }您好,\n
                                      您的密碼需要重新設定,\n
                                      請點入此連結重設密碼 : http://127.0.0.1:8000/account/password-reset/{urlsafe_base64_encode(force_bytes(user.id))}/{default_token_generator.make_token(user)}"""                              
                    email = EmailMessage(mailsubject, mailcontent, settings.EMAIL_HOST_USER, [mailto])
                    email.fail_silently = False
                    email.send()
    return render(request, 'forgetPassword.html', {'form':form})

@login_required
def profile(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'GET':
        return render(request,'profile.html',{'user':user})

@login_required
def profileUpdate(request, id):
    user = get_object_or_404(User, id=id)
    # if user is not owner
    if request.user.email != user.email:
        msg_error = "您沒有權限訪問此連結"
        return render(request, '403permission.html', {'user':user,'msg_error':msg_error})
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        print(form)
        if form.is_valid:
            user.fullName = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.website = form.cleaned_data['website']
            user.address = form.cleaned_data['address']
            user.save()
            return redirect(f'/account/profile/{user.id}/')
    else:
        original_data = {'username': user.fullName,
                         'email': user.email,
                         'website': user.website,
                         'address': user.address}
        form = ProfileForm(original_data)
    return render(request,'profileUpdate.html',{'form':form,'user':user})