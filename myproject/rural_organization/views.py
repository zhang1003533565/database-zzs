# RuralOrganization/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RuralOrganization
from .serializers import RuralOrganizationBasicSerializer

class RuralOrganizationBasicAPIView(APIView):
    def get(self, request):
        queryset = RuralOrganization.objects.all()
        serializer = RuralOrganizationBasicSerializer(queryset, many=True)
        return Response(serializer.data)
