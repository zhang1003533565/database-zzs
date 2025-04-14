# urls.py
from django.urls import path
from .views import RuralOrganizationBasicAPIView

urlpatterns = [
    path('api/ruralorganization/basic/', RuralOrganizationBasicAPIView.as_view()),
    #农业主要指标接口
]
