# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from apiuser.models import UserInfos

# Create your models here.


class Area(models.Model):
    """城区"""
    name = models.CharField(max_length=20, null=False)  # 区域名字


class House(models.Model):
    '''房屋信息'''
    user = models.ForeignKey(UserInfos, null=False)  # 房屋主人的用户编号
    area =  models.ForeignKey(Area, null=False)# 归属地的区域编号
    title =  models.CharField(max_length=20, null=False)  # 标题
    price = models.IntegerField(default=0) # 单价，单位：分
    address = models.CharField(max_length=60, default='')#   # 地址
    room_count = models.IntegerField(default=1)  # 房间数目
    acreage = models.IntegerField(default=0)  # 房屋面积
    unit = models.CharField(max_length=20, default='')  # 房屋单元， 如几室几厅
    capacity = models.IntegerField(default=1)  # 房屋容纳的人数
    beds = models.CharField(max_length=20, default='')  # 房屋床铺的配置
    deposit = models.IntegerField(default=0)  # 房屋押金
    min_days = models.IntegerField(default=1)  # 最少入住天数
    max_days = models.IntegerField(default=0)  # 最多入住天数，0表示不限制
    order_count = models.IntegerField(default=0)  # 预订完成的该房屋的订单数
    index_image_url = models.CharField(max_length=30, default='')  # 房屋主图片的路径
    #facilities = # db.relationship("Facility", secondary=house_facility)  # 房屋的设施
    #images = # db.relationship("HouseImage")  # 房屋的图片
    #orders =  #db.relationship("Order", backref="house")  # 房屋的订单


