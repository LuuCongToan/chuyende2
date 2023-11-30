from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=256)
    principal = models.CharField(max_length=256)
    location = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("basic_app:detail", kwargs={"pk": self.pk})
class Student(models.Model):
    name = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    school = models.ForeignKey(School,related_name='students',on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #additional
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic')
    bio = models.CharField(max_length=80,blank=True)
    nickname = models.CharField(max_length=80,blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_friends')
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_following')
    follower = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_follower')
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='user_blocked_users')
    def __str__(self):
        return self.user.username
class Post(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.user.username
    def num_comment(self):
        return self.comment_set.all().count()
    def num_like(self):
        return self.like_set.all().count()
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images',blank=True,null=True)
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class Like(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

# group
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='created_groups')
    ad_group = models.ManyToManyField(UserProfileInfo,blank=True)
    members = models.ManyToManyField(UserProfileInfo, related_name='joined_groups')
    def __str__(self):
        return self.name

class PostGroup(models.Model):
    title = models.CharField(max_length=100,blank=True)
    content = models.TextField(blank=True)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username
    def num_comment(self):
        return self.comment_set.all().count()
    def num_like(self):
        return self.like_set.all().count()
class ImageGroup(models.Model):
    post = models.ForeignKey(PostGroup, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images',blank=True,null=True)
class CommentGroup(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(PostGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# page
class Page(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='created_page')
    follow = models.ManyToManyField(UserProfileInfo, related_name='joined_page')
    ad_page = models.ManyToManyField(UserProfileInfo,blank=True)
    
    def __str__(self):
        return self.name 
class PostPage(models.Model):
    title = models.CharField(max_length=100,blank=True)
    content = models.TextField(blank=True)
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.user.username
    def num_comment(self):
        return self.comment_set.all().count()
    def num_like(self):
        return self.like_set.all().count()
class ImagePage(models.Model):
    post = models.ForeignKey(PostPage, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images',blank=True,null=True)
class CommentPage(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(PostPage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Đang chờ xác nhận'),
        ('accepted', 'Đã xác nhận'),
        ('rejected', 'Bị từ chối')
    ))
class Story(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    images = models.FileField(upload_to='images',blank=True,null=True)
    title = models.CharField(max_length=80,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
