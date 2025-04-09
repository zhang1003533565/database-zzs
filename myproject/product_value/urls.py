# product_value/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 视图函数
] 