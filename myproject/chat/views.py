from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .graph_flow import build_graph

app_graph = build_graph()

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("input", "")
            history = data.get("history", [])

            result = app_graph.invoke({
                "input": user_input,
                "output": "",
                "next": "",
                "history": history
            })

            return JsonResponse({
                "reply": result["output"],
                "history": result["history"]
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only POST allowed"}, status=405)
