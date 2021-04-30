from . import views
from django.urls import path
from django.conf.urls import url, include

app_name = 'user'
urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^profile/', views.profile_view, name='profile'),
    url(r'^update_user', views.UpdateUser.as_view(), name='update_user'),
    url(r'^update_passwd', views.UpdatePasswd.as_view(), name='update_passwd'),
    url(r'^logout', views.logout_view, name='logout'),
]