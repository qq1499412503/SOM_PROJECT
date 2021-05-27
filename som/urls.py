from . import views
from django.urls import path
from django.conf.urls import url, include

app_name = 'som'
urlpatterns = [
    url(r'^model', views.som_model, name='som_model'),
    url(r'^user_query_info', views.QueryUserInfo.as_view(), name='user_query_info'),
    url(r'^save_map', views.SaveMap.as_view(), name='save_map'),
    url(r'^save_and_publish', views.SaveAndPublish.as_view(), name='save_and_publish'),
    url(r'^test', views.test, name='test'),
    url(r'^tt', views.tt, name='tt'),
    url(r'^ChangeColor', views.ChangeColor.as_view(), name='ChangeColor'),
    
]