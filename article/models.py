from django.db import models
from django import forms
from account.models import User

class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    content = models.TextField()
    pubDateTime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)
    class Meta:
        db_table = 'Articles'

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    pubDateTime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Comments'

    def __str__(self):
        return self.article.title + '-' + str(self.id)
    
class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='標題', max_length=128)
    content = forms.CharField(label='內容', widget=forms.Textarea)
    class Meta:
        model = Article
        fields = ['title', 'content']


