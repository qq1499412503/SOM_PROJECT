from . import views
from django.urls import path
from django.conf.urls import url, include

app_name = 'som'
urlpatterns = [
    url(r'^$', views.som_model, name='som_model'),
    url(r'^user_query_info', views.QueryUserInfo.as_view(), name='user_query_info'),
]