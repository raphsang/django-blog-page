# Generated by Django 5.0.7 on 2024-07-31 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_introduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='introduction',
        ),
    ]
