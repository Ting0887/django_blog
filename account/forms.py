from msilib.schema import Class
from django import forms
from account.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(label='帳號')
    email = forms.CharField(label='電子郵件', widget=forms.EmailInput, max_length=128)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='確認密碼', widget=forms.PasswordInput)
    fullName = forms.CharField(label='姓名', max_length=128)
    website = forms.URLField(label='個人網址', max_length=128)
    address = forms.CharField(label='地址', max_length=128)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'fullName', 'website', 'address', 'email']
        
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('密碼不相符')
        return password2
    
    def clean_email(self):    
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise forms.ValidationError('此信箱已被註冊')
        return email
    
    def save(self):
        user = super().save(commit=False)
        user.set_password(user.password)
        user.save()
        return user

class ProfileForm(forms.Form):
    username = forms.CharField(label='帳號')
    email = forms.EmailField(label='電子郵件', max_length=128)
    website = forms.URLField(label='個人網址', max_length=128)
    address = forms.CharField(label='地址', max_length=128)
    
class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="電子郵件",max_length=256,
        widget  = forms.EmailInput(attrs={'id': 'email',"name":"email","placeholder":"Email","style":"width:250px ;height: 30px;"})
    )
    
class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
            label="新密碼",
            widget=forms.PasswordInput
            )
    password2 = forms.CharField(
            label="確認密碼",
            widget=forms.PasswordInput
    )
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("你的密碼太短")
        elif len(password1) > 20:
            raise forms.ValidationError("你的密碼太長")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("密碼不匹配")
        return password2