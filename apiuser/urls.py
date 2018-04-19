# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^users/$', views.register),
    url(r'^imagecode$', views.imagecode),
    url(r'^smscode/$', views.smscode),
    url(r'^sessions/$', views.login),  # 登陆
    url(r'^session/$', views.get_session),  # 获取登陆信息
    #url(r'^v1.0/houses/index$', views.get_houses),
]
