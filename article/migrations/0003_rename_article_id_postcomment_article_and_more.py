# Generated by Django 4.2.14 on 2024-07-25 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_postcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='article_id',
            new_name='article',
        ),
        migrations.AddField(
            model_name='postcomment',
            name='is_reply',
            field=models.BooleanField(default=False),
        ),
    ]
