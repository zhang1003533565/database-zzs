from django.urls import path
from .views import TechApplicationBasicAPIView

urlpatterns = [
    path('api/techapplication/basic/', TechApplicationBasicAPIView.as_view()),
] 