from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import hmac
import hashlib

SECRET_KEY = "DxFWESD234sf3DE2Ngfg459Ff"


@csrf_exempt
def transaction_listener(request):
    if request.method == "POST":
        try:
            transaction_body = json.loads(request.body)

            #signature from the header
            signature_from_request = request.headers.get("YAYA-SIGNATURE")
            if not signature_from_request: 
                return JsonResponse({"error": "Signature is not found"}, status = 400)
            

            concatnated_payload = "".join(str(each_values) for each_values in transaction_body.values())
            signed_payload = concatnated_payload.encode("utf-8")

            #hashing the signed payload
            yaya_signature = hmac.new(SECRET_KEY.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()

                    
            if not hmac.compare_digest(signature_from_request, yaya_signature):
                return JsonResponse({"error": "Signature didn't match"}, status = 401)

            print("the received transaction info: ", transaction_body)

            if transaction_body.get("event") == "transaction.confirmed":
                print("transaction confirmed! the next action will go here...")
                print("updating a customer’s invoice as paid....")

            return JsonResponse ({"status": "success"}, status = 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400)
        
    return JsonResponse({"error": "Invalid request"}, status = 400)