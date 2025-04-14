# serializers.py
from rest_framework import serializers
from .models import TechApplication

class TechApplicationBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechApplication
        fields = ['id', 'dmsyl', 'nysyl', 'jxhcd', 'sdjxhcd', 'sdjscd', 'dsjzx_taskid', 'jgmj', 'sdjmj', 'jdjsmj', 'hfsul', 'jz', 'dmfgmj']  # 可根据实际模型调整字段