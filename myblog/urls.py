"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from article.views import article_detail, create_article, delete_article, homepage
from account.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', homepage, name='Home'),
    path('create_article/', create_article, name='Create_Article'),
    path('article/<int:articleid>', article_detail, name='Article_Detail'),
    path('article/delete/<int:articleid>', delete_article, name='Delete_Article'),
    
    path('login/', login, name="Login"),
    path('logout/', logout, name="Logout"),
]
