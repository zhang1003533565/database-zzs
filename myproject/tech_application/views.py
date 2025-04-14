from .models import TechApplication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TechApplicationBasicSerializer

class TechApplicationBasicAPIView(APIView):
    def get(self, request):
        queryset = TechApplication.objects.all()
        serializer = TechApplicationBasicSerializer(queryset, many=True)
        return Response(serializer.data)
