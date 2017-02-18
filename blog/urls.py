"""Django_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^login/', views.login, name="Login"),
    url(r'^signin/', views.signin),
    url(r'^logout/', views.logout),
    url(r'^signin/', views.login),
    url(r'^index/', views.index),
    url(r'^notes/', views.notes),
    url(r'^addfavor/', views.addfavor),
    url(r'^getreply/', views.getreply),
    url(r'^submitreply/', views.submitreply),
    url(r'^addnote/', views.addnote),
    url(r'^addnotesuccess/', views.addnotesuccess),
    url(r'^signinsuccess/', views.signinsuccess),
    url(r'^chat/', views.chat),
    url(r'^sendchat/', views.sendchat),
    url(r'^getnewmessages/', views.get_new_messages, name="get_new_messages"),
    url(r'^uploadfile/', views.upload_file, name="upload_file"),
    # url(r'^uploadprogress/', views.upload_progress, name="upload_progress"),

]
