# serializers.py
from rest_framework import serializers
from .models import TotalAgriculture

class TotalAgricultureBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalAgriculture
        fields = ['id', 'dw', 'nyzz', 'dsjzx_taskid', 'zbmc', 'nyzcz', 'jhpt_update_time']  # 可根据实际模型调整字段