# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^user/$', views.register),
    url(r'^v1.0/imagecode$', views.imagecode),
    url(r'^v1.0/smscode/$', views.smscode)
]
