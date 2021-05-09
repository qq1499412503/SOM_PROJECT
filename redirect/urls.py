from . import views
from django.urls import path
from django.conf.urls import url, include


app_name = 'redirect'
urlpatterns = [
    url(r'^$', views.redirect_view, name='redirect'),
]