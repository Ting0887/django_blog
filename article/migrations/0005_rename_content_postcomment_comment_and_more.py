# Generated by Django 4.2.14 on 2024-07-25 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_rename_user_id_postcomment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='content',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='is_reply',
        ),
    ]