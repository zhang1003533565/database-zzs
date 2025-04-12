# urls.py
from django.urls import path
from .views import HealthBasicAPIView

urlpatterns = [
    path('api/health/basic/', HealthBasicAPIView.as_view()),
    #农村卫生组织接口
]
