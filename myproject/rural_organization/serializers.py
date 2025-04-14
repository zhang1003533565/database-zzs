# serializers.py
from rest_framework import serializers
from .models import RuralOrganization

class RuralOrganizationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuralOrganization
        fields = ['id', 'jz','cmxz','ncrk', 'cmwyh', 'dsjzx_taskid', 'ncjzrk', 'ncjzhs']  # 只返回你要的字段
