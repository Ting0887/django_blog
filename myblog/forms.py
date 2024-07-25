from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import re
from article.models import PostComment

class LoginForm(forms.Form):
    email = forms.CharField(
        label="帳號",max_length = 50,
        widget= forms.TextInput(attrs={'id':'email','placeholder':'帳號'})
    )
    password = forms.CharField(
        label="密碼",
        widget= forms.PasswordInput(attrs={'id':'password','placeholder':'密碼'})
    )
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_result = User.objects.filter(email=email)
        if len(filter_result) == 0:
            raise forms.ValidationError("使用者帳號不存在")
        return email
    
    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("密碼不正確")
        return password

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': '留言...', 'rows': 3}),
        }
        labels = {
            'comment': '留言',
        }