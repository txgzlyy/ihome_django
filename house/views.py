# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import transaction
from models import House,Area
from django.http import JsonResponse
from apiuser.utils.check import chech_get, chech_login
from apiuser.utils.response_code import RET
from apiuser.utils.qiniu_store import push_img
from apiuser.utils import constens

# Create your views here.


@chech_get
def get_area(req):
    areas = Area.objects.all()
    areas_data = [{'aid':area.id, 'aname':area.name} for area in areas]
    #  我们可以使用{% verbatim %} {% endverbatim %}包裹 禁用django魔板用于解决和js的冲突
    return JsonResponse({'errno':RET.OK, 'errmsg':'ok', 'data':areas_data})


@chech_login
@transaction.atomic
def houses(req):
    '''post 添加房源'''
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})

    get_datas = json.loads(req.body)
    if not get_datas:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '参数不完整'})
    user_id = req.session.get('user_id')
    area_id = get_datas.get('area_id')
    capacity = get_datas.get("capacity")  # 适合住几个人
    title = get_datas.get('title')
    price = get_datas.get('price')
    acreage = get_datas.get('acreage')  # 面积
    beds = get_datas.get('beds')
    room_count = get_datas.get('room_count')  # 房屋数量
    max_days = get_datas.get('max_days')
    deposit = get_datas.get('deposit')   # 押金
    address = get_datas.get('address')  # 详细地址
    min_days = get_datas.get("min_days")
    unit = get_datas.get('unit')  # 房屋单元
    facility = get_datas.get('facility')  # 设施

    house = House()
    house.user_id = user_id
    house.area_id = area_id
    house.capacity = capacity
    house.title = title
    house.price = price
    house.acreage = acreage
    house.beds = beds
    house.room_count = room_count
    house.max_days = max_days
    house.min_days = min_days
    house.deposit = deposit
    house.address = address
    house.unit = unit

    said = transaction.savepoint()
    try:
        house.save()
        transaction.savepoint_commit(said)
    except Exception as e:
        transaction.savepoint_rollback(said)
        return JsonResponse({'errno': RET.DBERR , 'errmsg': '数据库错误'})

    data = {"house_id": house.id}

    return JsonResponse({'errno': RET.OK, 'errmsg': 'ok', "data": data})


@chech_login
@transaction.atomic
def house_img(req, house_id):
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
    img_data = req.FILES.get("house_image").read()
    # 图片上传七牛
    try:
        index_img_name = push_img(img_data)['hash']
    except Exception as e:
        return JsonResponse({'errno': RET.THIRDERR, "errmsg": '第三方存贮错误'})
    index_img_url = constens.QINIU_IMG_URL + index_img_name
    # 图片名存入数据库
    said = transaction.savepoint()
    try:
        house = House.objects.filter(id=house_id).first()
        house.index_image_url = index_img_name
        house.save()
        transaction.savepoint_commit(said)
    except Exception as e:
        transaction.savepoint_rollback(said)
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库错误'})

    return JsonResponse({'errno': RET.OK, 'errmsg': 'ok','url':index_img_url})


@chech_get
@chech_login
def get_my_house(req):
    user_id = req.session.get('user_id')
    house_objs = House.objects.filter(user_id=user_id)
    if len(house_objs) == 0:
        return JsonResponse({'errno': RET.DATAERR, 'errmsg': 'ok'})
    houses = []
    for house in house_objs:
        houses.append(house.get_dict())

    return JsonResponse({'errno': RET.OK, 'errmsg': 'ok','houses': houses})





