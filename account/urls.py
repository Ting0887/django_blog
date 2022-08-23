from re import template
from django.urls import path, reverse_lazy
from account import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profileUpdate/<int:id>/', views.profileUpdate, name='profileUpdate'),
    
    path('forgetPassword/', views.forgetPassword, name='accounts/forgetPassword'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/passwordResetConfirm.html',
                                                     success_url='/account/password_reset_complete/'),
         name="password_reset_confirm"),
     path('password_reset_complete/',
          auth_views.PasswordResetCompleteView.as_view(template_name='accounts/passwordResetComplete.html')
         ,name="password_reset_complete"),
]
