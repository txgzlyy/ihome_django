# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apiuser.utils.check import chech_get
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.


@chech_get
@ensure_csrf_cookie
def index(req):
    return render(req,'index.html')


@chech_get
def auth(req):
    return render(req,'auth.html')


@chech_get
def booking(req):
    return render(req,'booking.html')


@chech_get
def detail(req):
    return render(req,'detail.html')


@chech_get
def login(req):
    return render(req,'login.html')


@chech_get
def lorders(req):
    return render(req,'lorders.html')


@chech_get
def my(req):
    return render(req,'my.html')


@chech_get
def myhouse(req):
    return render(req,'myhouse.html')


@chech_get
def newhouse(req):
    return render(req,'newhouse.html')


@chech_get
def orders(req):
    return render(req,'orders.html')


@chech_get
def profile(req):
    return render(req,'profile.html')


@ensure_csrf_cookie
@chech_get
def register(req):
    return render(req,'register.html')


def search(req):
    return render(req,'search.html')












