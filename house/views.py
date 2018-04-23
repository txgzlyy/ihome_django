# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import House,Area
from django.http import JsonResponse
from apiuser.utils.check import chech_get
from apiuser.utils.response_code import RET

# Create your views here.


@chech_get
def get_area(req):
    areas = Area.objects.all()
    areas_data = [{'aid':area.id, 'aname':area.name} for area in areas]
    #  我们可以使用{% verbatim %} {% endverbatim %}包裹 禁用django魔板用于解决和js的冲突
    return JsonResponse({'errno':RET.OK, 'errmsg':'ok', 'data':areas_data})