from django.shortcuts import render
from django.http import HttpResponse
from .models import TotalAgriculture

# Create your views here.

# 简单的视图函数
def index(request):
    return HttpResponse("欢迎访问农业总产值数据页面!")
