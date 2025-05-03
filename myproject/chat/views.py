# chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .graph_flow import build_graph
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

app_graph = build_graph()

class ChatAPIView(APIView):
    permission_classes = [AllowAny]  # ✅ 允许匿名访问

    @swagger_auto_schema(
        operation_description="聊天 API 接口",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['input'],
            properties={
                'input': openapi.Schema(type=openapi.TYPE_STRING, description='用户输入的消息'),
                'history': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description='聊天历史记录')
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'reply': openapi.Schema(type=openapi.TYPE_STRING, description='AI 回复的消息'),
                    'history': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description='更新后的聊天历史记录')
                }
            )
        }
    )
    def post(self, request):
        try:
            data = request.data
            user_input = data.get("input", "")
            history = data.get("history", [])

            result = app_graph.invoke({
                "input": user_input,
                "output": "",
                "next": "",
                "history": history
            })

            return Response({
                "reply": result["output"],
                "history": result["history"]
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
