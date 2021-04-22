from . import views
from django.urls import path
from django.conf.urls import url, include

app_name = 'publish'
urlpatterns = [
    url(r'^list/', views.publish_view, name='list'),
    url(r'^view/', views.view_view, name='view'),
]