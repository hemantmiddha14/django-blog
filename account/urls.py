from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

]
