# Generated by Django 4.2.5 on 2023-11-24 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0016_page_ad_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('content', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.userprofileinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ImagePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.FileField(blank=True, null=True, upload_to='images')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.postpage')),
            ],
        ),
        migrations.CreateModel(
            name='CommentPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.userprofileinfo')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.postpage')),
            ],
        ),
    ]
