from django.contrib import admin
from .models import HealthOrganization

@admin.register(HealthOrganization)
class HealthOrganizationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HealthOrganization._meta.fields]
    list_per_page = 20
    search_fields = ['name']  # 假设有name字段，请根据实际模型调整
    list_filter = ['created_at'] if hasattr(HealthOrganization, 'created_at') else []
    
    fieldsets = (
        ('基本信息', {
            'fields': [field.name for field in HealthOrganization._meta.fields if field.name != 'id']
        }),
    )
    
    # 设置模型的显示名称
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display_links = (self.list_display[0],)
    
    # 自定义列名显示
    def get_list_display(self, request):
        # 这里可以自定义列名的显示，如果需要的话
        return self.list_display
