# Generated by Django 2.0.3 on 2018-06-08 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Messages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
