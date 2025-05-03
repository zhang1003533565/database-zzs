"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 修改管理界面标题
admin.site.site_header = '青浦农业后台管理平台'
admin.site.site_title = '青浦农业后台管理平台'
admin.site.index_title = '欢迎使用青浦农业后台管理系统'

# 配置 Swagger 文档
schema_view = get_schema_view(
    openapi.Info(
        title="青浦农业 API 文档",
        default_version='v1',
        description="青浦农业后台管理平台 API 接口文档",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 同时支持 /docs 和 /swagger 路径
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-docs-ui'),
    path('docs.json/', schema_view.without_ui(cache_timeout=0), name='schema-docs-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # 您现有的 URL 配置
    path('', include('rural_organization.urls')),
    path('', include('health_organization.urls')),  # ✅ 农村卫生组织
    path('', include('main_index.urls')),  # ✅ 农业主要指标
    path('', include('product_value.urls')),  # ✅ 农业商品产值和商品率
    path('', include('rural_organization.urls')),  # ✅ 农村基层组织情况
    path("", include("chat.urls")),  # ✅ 添加这行
    path('', include('tech_application.urls')),  # 农业技术应用
    path('', include('total_agriculture.urls')),  # 农业总产值
    path('', include('total_value.urls')),  # 农业历年总产值
]
