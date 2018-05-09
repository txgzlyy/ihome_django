# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from apiuser.models import UserInfos
from apiuser.utils import constens

# Create your models here.


class Area(models.Model):
    """城区"""
    name = models.CharField(max_length=20, null=False)  # 区域名字


class Facilitys(models.Model):
    '''房屋设施'''
    facility = models.CharField(max_length=20,null=False)



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
    #  auto_now=False  修改时候时间不会更新
    create_time = models.DateTimeField(auto_now=False, default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    # house 和 facility 多对多
    facility = models.ManyToManyField(Facilitys)
    #orders =  #db.relationship("Order", backref="house")  # 房屋的订单
    def get_dict(self):
        data = {
            'house_id':self.id,
            'title': self.title,
            'index_image_url':constens.QINIU_IMG_URL+self.index_image_url,
            'area_name':self.area.name,
            'price':self.price,
            'ctime':self.create_time
        }
        return data

    def get_full_datas(self):
        img_urls = []  # 房屋展示图片
        # self.houseimages_set.all() house_id 是图片标的外键   反查操作
        for house_img_obj in self.houseimages_set.all():
            img_urls.append(constens.QINIU_IMG_URL+house_img_obj.img_name)
        facilitys = []
        for facility in self.facility.all():
            facilitys.append(facility.id)
        data = {
            'hid':self.id,
            'title': self.title,
            'img_urls':img_urls,
            'area_name':self.area.name,
            'price':self.price,
            'user_avatar':constens.QINIU_IMG_URL+self.user.avator,
            'user_name': self.user.name,
            'address': self.address,
            'room_count': self.room_count,
            'acreage': self.acreage,
            'unit': self.unit,
            'capacity': self.capacity,
            'beds': self.beds,
            'deposit': self.deposit*100,
            'min_days': self.min_days,
            'max_days': self.max_days,
            'facilities':facilitys
        }
        return data


class HouseImages(models.Model):
    '''房屋图片'''
    img_name = models.CharField(max_length=40, default='')
    house = models.ForeignKey(House, null=False)  # 房屋的图片
















