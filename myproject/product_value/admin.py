from django.contrib import admin
from .models import ProductValue

@admin.register(ProductValue)
class ProductValueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductValue._meta.fields]
    list_per_page = 20
    search_fields = ['name']  # 假设有name字段，请根据实际模型调整
    list_filter = ['created_at'] if hasattr(ProductValue, 'created_at') else []
    
    fieldsets = (
        ('基本信息', {
            'fields': [field.name for field in ProductValue._meta.fields if field.name != 'id']
        }),
    )
