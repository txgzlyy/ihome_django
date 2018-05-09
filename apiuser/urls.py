# coding=utf-8
from django.conf.urls import url
import views
from house.views import *

urlpatterns = [
    url(r'^users/$', views.register),
    url(r'^user/$', views.get_user),  # 页面加载想后端查询用户信息
    url(r'^user/name$', views.change_username),  # 页面加载想后端查询用户信息
    url(r'^user/avatar$', views.up_avator),
    url(r'^user/auth$', views.user_auth),
    url(r'^user/houses', get_my_house),
    url(r'^imagecode$', views.imagecode),
    url(r'^smscode/$', views.smscode),
    url(r'^sessions/$', views.login),  # 登陆
    url(r'^session/$', views.get_session),  # 获取登陆信息
    url(r'^areas$', get_area),
    url(r'^houses$', houses),
    url(r'^houses/(\d+)/images$', house_img),
]
