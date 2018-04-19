# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def indexs(req):
    return render(req,'index.html')

def auth(req):
    return render(req,'auth.html')

def booking(req):
    return render(req,'booking.html')


def detail(req):
    return render(req,'detail.html')

def login(req):
    return render(req,'login.html')

def lorders(req):
    return render(req,'lorders.html')

def my(req):
    return render(req,'my.html')

def myhouse(req):
    return render(req,'myhouse.html')

def newhouse(req):
    return render(req,'newhouse.html')

def orders(req):
    return render(req,'orders.html')

def profile(req):
    return render(req,'profile.html')

def register(req):
    return render(req,'register.html')

def search(req):
    return render(req,'search.html')












