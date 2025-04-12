# serializers.py
from rest_framework import serializers
from .models import HealthOrganization

class HealthBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthOrganization
        fields = ['id', 'zhen', 'xcyss', 'xzcs', 'dsjzx_taskid']  # 只返回你要的字段
