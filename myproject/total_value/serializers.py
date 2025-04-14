# serializers.py
from rest_framework import serializers
from .models import TotalValue

class TotalValueBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TotalValue
        fields = ['id', 'yy', 'fy', 'nlmyfwy', 'ly', 'dsjzx_taskid', 'year', 'my', 'zzy', 'nyzcz']  # 可根据实际模型调整字段