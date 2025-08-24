from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def transaction_listener(request):
    if request.method == "POST":
        try:
            transaction_body = json.loads(request.body)

            print("the received transaction info: ", transaction_body)

            if transaction_body.get("event") == "transaction.confirmed":
                print("transaction confirmed! the next action will go here...")

            return JsonResponse ({"status": "success"}, status = 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400)
        
    return JsonResponse({"error": "Invalid request"}, status = 400)