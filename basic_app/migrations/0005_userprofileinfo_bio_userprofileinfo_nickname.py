# Generated by Django 4.2.5 on 2023-11-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0004_alter_story_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='bio',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]