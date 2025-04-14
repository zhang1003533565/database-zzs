# serializers.py
from rest_framework import serializers
from .models import ProductValue

class ProductValueBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductValue
        fields = ['id', 'dw','ze_last_year','ze2023', 'zb', 'dsjzx_taskid']  # 只返回你要的字段
