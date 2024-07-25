from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,default='')
    content = models.TextField()
    
    class Meta:
        db_table = 'article'
    
    def __str__(self):
        return self.title


class PostComment(models.Model):
    article= models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # 父评论
    comment = models.TextField()  # 留言或回复内容
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comment'
        ordering = ['timestamp']

    def __str__(self):
        return f"Comment by {self.user} on article '{self.article}'"