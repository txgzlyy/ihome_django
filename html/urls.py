# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^auth/$', views.auth),
    url(r'^booking/$', views.booking),
    url(r'^detail/$', views.detail),
    url(r'^login/$', views.login),
    url(r'^lorders/$', views.lorders),
    url(r'^my/$', views.my),
    url(r'^myhouse/$', views.myhouse),
    url(r'^orders/$', views.orders),
    url(r'^profile/$', views.profile),
    url(r'^register/$', views.register),
    url(r'^search/$', views.search),
]