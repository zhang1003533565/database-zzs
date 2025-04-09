from django.shortcuts import render
from django.http import HttpResponse
from .models import TechApplication

# Create your views here.

# 简单的视图函数
def index(request):
    return HttpResponse("欢迎访问农业技术应用数据页面!")
