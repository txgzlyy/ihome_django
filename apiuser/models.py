# coding=utf-8
from django.db import models
from django.utils import timezone

# Create your models here.


class UserInfos(models.Model):
    name = models.CharField(max_length=20, default='')
    mobile = models.CharField(max_length=11, null=False)
    password = models.CharField(max_length=40, null=False)
    avator = models.CharField(max_length=60, default='')
    relname = models.CharField(max_length=20, default='')   # 实名认证
    id_card = models.CharField(max_length=18, default='')

    #  auto_now=False  修改时候时间不会更新
    create_time = models.DateTimeField(auto_now=False, default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
