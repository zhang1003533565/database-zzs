# health_organization/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HealthOrganization
from .serializers import HealthBasicSerializer

class HealthBasicAPIView(APIView):
    def get(self, request):
        queryset = HealthOrganization.objects.all()
        serializer = HealthBasicSerializer(queryset, many=True)
        return Response(serializer.data)
