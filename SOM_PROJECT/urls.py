"""SOM_PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.static import serve
from .settings import MEDIA_ROOT
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', include('redirect.urls', namespace='redirect')),
    url(r'^som/', include('som.urls', namespace='som')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^publish/', include('publish.urls', namespace='publish')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})
    # url(r'^jasmine-test-suite/', include('django_jasmine.urls'))

]
