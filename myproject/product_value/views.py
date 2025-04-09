from django.shortcuts import render
from django.http import HttpResponse
from .models import ProductValue

# Create your views here.

# 简单的视图函数
def index(request):
    return HttpResponse("欢迎访问农业商品产值和商品率数据页面!")
