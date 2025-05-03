# health_organization/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HealthOrganization
from .serializers import HealthBasicSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class HealthBasicAPIView(APIView):
    @swagger_auto_schema(
        operation_description="获取所有健康组织数据",
        responses={200: HealthBasicSerializer(many=True)}
    )
    def get(self, request):
        queryset = HealthOrganization.objects.all()
        serializer = HealthBasicSerializer(queryset, many=True)
        return Response(serializer.data)
