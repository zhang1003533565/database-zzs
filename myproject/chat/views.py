# chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .graph_flow import build_graph

app_graph = build_graph()

class ChatAPIView(APIView):
    permission_classes = [AllowAny]  # ✅ 允许匿名访问

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
