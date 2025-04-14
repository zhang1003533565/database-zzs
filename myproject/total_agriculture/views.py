from .models import TotalAgriculture
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TotalAgricultureBasicSerializer

class TotalAgricultureBasicAPIView(APIView):
    def get(self, request):
        queryset = TotalAgriculture.objects.all()
        serializer = TotalAgricultureBasicSerializer(queryset, many=True)
        return Response(serializer.data)
