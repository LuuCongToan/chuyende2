# Generated by Django 4.2.5 on 2023-11-25 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0017_postpage_imagepage_commentpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, related_name='user_blocked_users', to='basic_app.userprofileinfo'),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='user_follower', to='basic_app.userprofileinfo'),
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='user_following', to='basic_app.userprofileinfo'),
        ),
    ]
