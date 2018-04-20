# coding=utf-8
import random
import json
import re
from django.db import transaction
from hashlib import sha1
from models import UserInfos
from django.http import HttpResponse, JsonResponse
from utils.captcha.captcha import captcha
# redis缓存
from utils.redis_store import redis_store
from utils import constens
from utils.response_code import RET
from utils.sms_code import CCP
from utils.check import chech_get, chech_login
from utils.qiniu_store import push_img

# Create your views here.


@transaction.atomic
def register(req):
    '''GET请求为战士注册页  POST请求发送注册请求'''
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
    data = json.loads(req.body)  # 获取post数据  {"mobile": mobile,"password": passwd,"sms_code": phoneCode}
    mobile = data.get("mobile")
    password = data.get("password")
    sms_code = data.get("sms_code")

    # 手机号格式校验
    if not re.match(r"1[34578]\d{9}$", mobile):
        return JsonResponse({'errno':RET.PARAMERR, 'errmsg':"手机号格式不正确"})
    # 检验短信验证码正确性
    try:
        redis_sms_code = redis_store.get("sms_code" + mobile)
        # 删除redis中的验证码
        redis_store.delete("sms_code" + mobile)
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库异常'})

    if redis_sms_code != sms_code:
        return JsonResponse({'errno':RET.DATAERR, 'errmsg':"短信验证码不正确"})

    # 检验手机号是否存在
    try:
        user = UserInfos.objects.filter(mobile=mobile).first()
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库异常'})

    if user is not None:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '手机号已存在'})

    # 密码加密
    password_hash = sha1(password).hexdigest()
    print password_hash

    user_save = UserInfos(mobile=mobile, password=password_hash, name=mobile)
    # 创建事务 sid
    said = transaction.savepoint()
    try:
        user_save.save()
    except Exception as e:
        transaction.savepoint_rollback(said)
        return JsonResponse({'errno': RET.DBERR, "errmsg": '保存数据库失败'})

    transaction.savepoint_commit(said)  # 提交事务

    # 保存注册信息
    req.session["user_id"] = user_save.id
    req.session['user_name'] = user_save.name
    req.session['mobile'] = mobile

    return JsonResponse({'errno': RET.OK, "errmsg": '注册成功！'})


@chech_get
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
    '''短信验证码'''
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
    data = json.loads(req.body)
    mobile = data.get('mobile')  # 手机号
    text = data.get("text") # 图片验证码
    img_id = data.get("id")  # 图片验证码编号
    if not all([mobile, text, id]):
        return JsonResponse({'errno':RET.PARAMERR,"errmsg":'参数不完整'})

    # 验证图片验证码正确性
    try:
        redis_img_code = redis_store.get('image_code'+img_id)
        # 删除redis中的验证码
        redis_store.delete('image_code'+img_id)
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库异常'})

    if text != redis_img_code:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '图片验证码不正确'})

    # 检验手机号是否存在
    try:
        user = UserInfos.objects.filter(mobile=mobile).first()
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库异常'})

    if user is not None:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '手机号已存在'})

    # 发送短信验证码
    # 生成短信验证码
    sms_code = '%06d' % random.randint(0, 1000000)
    try:
        redis_store.setex('sms_code'+mobile,constens.SMS_CHECK_TIME,sms_code)
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库异常'})

    # 发送短信验证码
    ccp = CCP()
    try:
        res = ccp.send_sms(mobile, [sms_code,constens.SMS_CHECK_TIME], 1)
    except Exception as e:
        return JsonResponse({'errno': RET.THIRDERR, "errmsg": '短信验证码发第三方错误'})

    if 0 == res:
        return JsonResponse({'errno': RET.OK, "errmsg": '短信验证码发送成功'})
    else:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '短信验证码发送失败'})


def login(req):
    '''登陆'''
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
    data = json.loads(req.body)
    mobile = data.get("mobile")
    password = data.get("password")
    if not all([mobile,password]):
        return JsonResponse({'errno': RET.PARAMERR, "errmsg": '参数不完整'})

    # 手机号格式校验
    if not re.match(r"1[34578]\d{9}$", mobile):
        return JsonResponse({'errno': RET.PARAMERR, 'errmsg': "手机号格式不正确"})
    try:
        user = UserInfos.objects.filter(mobile=mobile).first()
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, 'errmsg': "数据库异常"})

    if user is None:
        return JsonResponse({'errno': RET.DATAERR, 'errmsg': "手机号未注册"})
    # 检验密码
    password_hash = sha1(password).hexdigest()
    if password_hash != user.password:
        return JsonResponse({'errno': RET.DATAERR, 'errmsg': "密码不正确"})

    # 保存登陆信息
    req.session["user_id"] = user.id
    req.session['user_name'] = user.name
    req.session['mobile'] = mobile

    return JsonResponse({'errno': RET.OK, "errmsg": 'OK'})


@chech_get
@chech_login
def get_session(req):
    '''获取登陆信息'''
    user_id = req.session.get('user_id')
    try:
        user = UserInfos.objects.filter(id=user_id).first()
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库查询错误'})
    if not user:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '信息有误'})
    name = user.name
    data = {'name':name}
    return JsonResponse({'errno': RET.OK, "errmsg": 'OK','data':data})


@chech_get
@chech_login
def get_user(req):
    '''获取用户信息'''
    user_id = req.session.get('user_id')
    try:
        user = UserInfos.objects.filter(id=user_id).first()
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库查询错误'})
    if not user:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '信息有误'})
    name = user.name
    avator = constens.QINIU_IMG_URL + user.avator
    mobile = user.mobile

    data = {'name':name, "mobile":mobile, "avatar":avator}
    return JsonResponse({'errno': RET.OK, "errmsg": 'OK','data':data})


@chech_login
@transaction.atomic
def change_username(req):
    '''修改用户名'''
    if req.method != 'PUT':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
    user_id = req.session.get('user_id')
    data = json.loads(req.body)
    name = data.get("name")
    if name is None:
        return JsonResponse({'errno': RET.PARAMERR, "errmsg": '参数缺失'})

    said = transaction.savepoint()
    try:
        user = UserInfos.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'errno': RET.DATAERR, "errmsg": '信息有误'})
        user.name = name
        user.save()
    except Exception as e:
        transaction.savepoint_rollback(said)
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库查询错误'})
    # 提交保存
    transaction.savepoint_commit(said)

    return JsonResponse({'errno': RET.OK, "errmsg": 'OK'})


@chech_login
@transaction.atomic
def up_avator(req):
    '''上传头像'''
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})

    user_id = req.session.get('user_id')

    img_data = req.FILES.get("avatar").read()   # 接受二进制数据   .read() 注意

    try:
        avatar_url = push_img(img_data)
        avatar_url = avatar_url['hash']
    except Exception as e:
        return JsonResponse({'errno':RET.THIRDERR, 'errmsg':'第三方程序错误'})
    # 把图片url 存入数据库

    said = transaction.savepoint()
    try:
        user = UserInfos.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'errno': RET.DATAERR, "errmsg": '信息有误'})
        user.avator = avatar_url
        user.save()
    except Exception as e:
        transaction.savepoint_rollback(said)
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库查询错误'})
    transaction.savepoint_commit(said)

    data = {"avatar_url": constens.QINIU_IMG_URL+avatar_url}
    return JsonResponse({'errno': RET.OK, "errmsg": 'OK', 'data': data})



@chech_login
@transaction.atomic
def user_auth(req):
    '''实名认证'''
    user_id = req.session["user_id"]
    try:
        user = UserInfos.objects.filter(id=user_id).first()
    except Exception as e:
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库查询错误'})
    if not user:
        return JsonResponse({'errno': RET.DATAERR, "errmsg": '信息有误'})
    # 读取
    if req.method == 'GET':
        relname = user.relname
        id_card = user.id_card
        data = {"real_name": relname, "id_card":id_card}
        return JsonResponse({'errno': RET.OK, "errmsg": 'OK', 'data': data})

    # 修改
    if req.method != 'POST':
        return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
    data = json.loads(req.body)
    relname = data.get("real_name")
    id_card = data.get("id_card")
    if not all([relname,id_card]):
        return JsonResponse({'errno': RET.PARAMERR, "errmsg": '参数不完整'})
    user.relname = relname
    user.id_card = id_card

    said = transaction.savepoint()
    try:
        user.save()
    except Exception as e:
        transaction.savepoint_rollback(said)
        return JsonResponse({'errno': RET.DBERR, "errmsg": '数据库查询错误'})
    transaction.savepoint_commit(said)
    return JsonResponse({'errno': RET.OK, "errmsg": 'ok'})



