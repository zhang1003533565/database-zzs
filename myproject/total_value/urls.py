# total_value/urls.py
from django.urls import path
from .views import TotalValueBasicAPIView

urlpatterns = [
    path('api/totalvalue/basic/', TotalValueBasicAPIView.as_view()),
] 