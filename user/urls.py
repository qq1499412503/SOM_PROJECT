from . import views
from django.urls import path
from django.conf.urls import url, include

app_name = 'user'
urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^register/', views.register_view, name='register'),
]