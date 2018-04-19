from django.db import models

# Create your models here.

class UserInfos(models.Model):
    name = models.CharField(max_length=20, default='')
    mobile = models.CharField(max_length=11, null=False)
    password = models.CharField(max_length=40, null=False)