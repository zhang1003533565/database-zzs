# urls.py
from django.urls import path
from .views import ProductValueBasicAPIView

urlpatterns = [
    path('api/productvalue/basic/', ProductValueBasicAPIView.as_view()),
    #农业主要指标接口
]
