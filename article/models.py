from django.db import models

# Create your models here.

class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,default='')
    content = models.TextField()
    
    class Meta:
        db_table = 'article'
    
    def __str__(self):
        return self.title