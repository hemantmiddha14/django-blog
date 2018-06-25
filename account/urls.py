from django.conf.urls import url
from . import views
from django.http import HttpResponse, HttpRequest

app_name = 'account'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
	url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
]
