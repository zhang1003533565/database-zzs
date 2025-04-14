# chat/urls.py 或 myproject/urls.py
from django.urls import path
from .views import ChatAPIView

urlpatterns = [
    path('api/chat/', ChatAPIView.as_view()),
]
