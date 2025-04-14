# total_agriculture/urls.py
from django.urls import path
from .views import TotalAgricultureBasicAPIView

urlpatterns = [
    path('api/totalagriculture/basic/', TotalAgricultureBasicAPIView.as_view()),
] 