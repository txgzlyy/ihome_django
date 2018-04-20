# coding=utf-8
from django.http import HttpResponseRedirect, JsonResponse
from response_code import RET


def chech_login(func):
    def inner(request,*args,**kwargs):
        # path = request.get_full_path()
        # paths = [
        #     '/',
        #     '/v1.0/users/',
        #     '/v1.0/imagecode',
        #     '/v1.0/smscode/',
        #     '/v1.0/sessions/',
        #     '/v1.0/session/',
        # ]
        if not request.session.get('user_id'):
            return HttpResponseRedirect('/html/login/')
        return func(request,*args,**kwargs)
    return inner


def chech_get(func):
    def inner(request,*args,**kwargs):
        if request.method != 'GET':
            return JsonResponse({'errno': RET.REQERR, "errmsg": '请求方式不允许'})
        return func(request,*args,**kwargs)
    return inner