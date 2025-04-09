# rural_organization/views.py
from django.shortcuts import render
from django.http import HttpResponse

# 简单的视图函数
def index(request):
    return HttpResponse("Welcome to Rural Organization Data!")
