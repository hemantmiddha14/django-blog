from django.conf.urls import url
from . import views
from account import views as account_view
from Profile import views as profile_view

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/del/$', views.post_del, name='post_del'),
    url(r'^register/$', account_view.register, name='register'),
    url(r'^edit_profile/$', profile_view.edit_profile, name='edit_profile'),

]
