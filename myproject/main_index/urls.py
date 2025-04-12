# urls.py
from django.urls import path
from .views import MainIndexBasicAPIView

urlpatterns = [
    path('api/mainindex/basic/', MainIndexBasicAPIView.as_view()),
    #农业主要指标接口
]
