# ProductValue/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProductValue
from .serializers import ProductValueBasicSerializer

class ProductValueBasicAPIView(APIView):
    def get(self, request):
        queryset = ProductValue.objects.all()
        serializer = ProductValueBasicSerializer(queryset, many=True)
        return Response(serializer.data)
