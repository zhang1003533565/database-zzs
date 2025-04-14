from .models import TotalValue
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TotalValueBasicSerializer

class TotalValueBasicAPIView(APIView):
    def get(self, request):
        queryset = TotalValue.objects.all()
        serializer = TotalValueBasicSerializer(queryset, many=True)
        return Response(serializer.data)
