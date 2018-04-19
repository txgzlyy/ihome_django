# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.indexs),
    url(r'^v1.0/users/$', views.register),
    url(r'^v1.0/imagecode$', views.imagecode),
    url(r'^v1.0/smscode/$', views.smscode),
    url(r'^v1.0/session/', views.get_session),  # 获取登陆信息
]
