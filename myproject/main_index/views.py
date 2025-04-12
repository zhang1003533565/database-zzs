# MainIndex/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MainIndex
from .serializers import MainIndexBasicSerializer

class MainIndexBasicAPIView(APIView):
    def get(self, request):
        queryset = MainIndex.objects.all()
        serializer = MainIndexBasicSerializer(queryset, many=True)
        return Response(serializer.data)
