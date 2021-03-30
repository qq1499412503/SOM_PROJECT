from . import views
from django.urls import path
from django.conf.urls import url, include

app_name = 'som'
urlpatterns = [
    url(r'^$', views.som_model, name='som_model'),
    path('sample_api', views.sample_api.as_view(), name='sample_test_case'),

]