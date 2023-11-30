from django.urls import re_path,path,include
from basic_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'basic_app'

urlpatterns = [
    # re_path(r'^$',views.SchoolListView.as_view(),name='list'),
    # re_path(r'^$',views.SchoolListView.as_view(),name='list'),

    re_path(r'^(?P<pk>\d+)/$',views.SchoolDetailView.as_view(),name='detail'),
    re_path(r'^create/$',views.SchoolCreateView.as_view(),name='create'),
    re_path(r'^update/(?P<pk>\d+)/$',views.SchoolUpdateView.as_view(),name='update'),
    re_path(r'^delete/(?P<pk>\d+)/$',views.SchoolDeleteView.as_view(),name='delete'),

    re_path(r'^register/$',views.register,name='register'),
    re_path(r'^user_login/$',views.user_login,name='user_login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^index/$', views.profileindex, name='profileindex'),
    re_path(r'^post_create/$', views.create_post, name='create_post'),
    
    # re_path(r'^profile/$', views.posts_list, name='profile'),
   
    # re_path(r'^login/$', views.login, name='user_login'), 
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

