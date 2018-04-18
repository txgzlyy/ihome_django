# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .utils.captcha.captcha import captcha
# redis缓存
from .utils.redis_store import redis_store
from .utils import constens

# Create your views here.


def register(req):
    return render(req, 'register.html')


def imagecode(req):
    '''生成图片验证码'''
    # 上一次img id
    pre_imgcode = req.GET.get("pre")
    # 当前img_id
    cur_imgcode = req.GET.get("cur")
    if not cur_imgcode:
        return HttpResponse("参数不正确")

    # 生成验证码  img 二进制数据流
    name, txt, img = captcha.generate_captcha()

    try:
        # 删除上一次缓存
        redis_store.delete('image_code'+pre_imgcode)
        # setex(name, time, value):
        redis_store.setex('image_code'+cur_imgcode, constens.IMG_CHECK_TIME, txt)
    except Exception as e:
        return HttpResponse("数据缓存失败")
    # 类容格式  "image/png"
    return HttpResponse(img, "image/png")


def smscode(req):
    return HttpResponse("ok")