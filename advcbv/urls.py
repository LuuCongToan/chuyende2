"""
URL configuration for advcbv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path,include,path
from basic_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^admin/', admin.site.urls,name= 'admin'),
    re_path(r'^basic_app/',include('basic_app.urls',namespace='basic_app')),
    re_path(r'^logout/$',views.user_logout,name='logout'),

    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^index/$', views.profileindex, name='profileindex'),
    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^$', views.user_login, name='user_login'),
    re_path(r'^post_create/$', views.create_post, name='create_post'),
    re_path(r'^like_post/$', views.like_post, name='like_post'),

    re_path(r'^all_groups/$', views.all_groups, name='all_groups'),
    re_path(r'^groups/<int:pk>/delete/$', views.delete_group, name='delete_group'),
    re_path(r'^groups/<int:group_id>/edit/$', views.edit_group, name='edit_group'),
    path('groupindex/<int:id>/', views.groupindex, name='groupindex'),
    path('group_members/<int:id>/', views.group_member, name='group_members'),

    re_path(r'^all_page/$', views.all_page, name='all_page'),
    re_path(r'^page/<int:page_id>/edit/$', views.edit_page, name='edit_page'),
    re_path(r'^page/<int:pk>/delete/$', views.delete_page, name='delete_page'),
    path('page_index/<int:id>/', views.page_index, name='page_index'),
    path('page_follow/<int:id>/', views.page_follow, name='page_follow'),


    re_path(r'^post/<int:pk>/delete/$', views.delete_post, name='delete_post'),
    re_path(r'^post/<int:pk>/edit/$', views.edit_post, name='edit_post'),
    re_path(r'^search/$', views.search, name='search'),
    path('other_profile/<int:id>/', views.other_profile, name='other_profile'),
    path('setting', views.setting_profile, name='setting'),
    path('delete_stories/', views.delete_stories, name='delete_stories'),

    
    path('add_friend/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('delete_friend/<int:friend_id>/', views.delete_friend, name='delete_friend'),
    # path('view_profile/<int:id>/', views.other_profile, name='view_profile'),
    re_path(r'^friends$', views.friends, name='friends'),

    path('list_follow/<int:user_id>/', views.list_follow, name='list_follow'),
    path('list_followings/<int:user_id>/', views.list_followings, name='list_followings'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow_user/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('list_block/<int:user_id>/', views.list_block, name='list_block'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
