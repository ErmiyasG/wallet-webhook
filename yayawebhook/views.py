from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import hmac
import hashlib
from django.conf import settings
import time
from decouple import config

SECRET_KEY = config("SIGNATURE_SECRET_KEY")

def signatureMaker(payload: dict, secret_key: str) -> str:

    concatnated_payload = "".join(str(each_values) for each_values in payload.values())
    signed_payload = concatnated_payload.encode("utf-8")

    #hashing the signed-payload
    yaya_signature = hmac.new(secret_key.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()

    return yaya_signature


@csrf_exempt
def transaction_listener(request):
    if request.method == "POST":
        try:
            transaction_body = json.loads(request.body)

            #signature from the header
            signature_from_request = request.headers.get("YAYA-SIGNATURE")
            
            if not signature_from_request: 
                return JsonResponse({"error": "Signature is not found"}, status = 400)
            
            actual_signature = signatureMaker(transaction_body, SECRET_KEY)

            if not hmac.compare_digest(signature_from_request, actual_signature):
                return JsonResponse({"error": "Signature didn't match"}, status = 401)
            

            #checking the timestamp tolerance
            tolerance_seconds = getattr(settings, "YAYA_TOLERANCE_SECONDS", 300)  # default 5 min tolerance
            current_time = int(time.time())
            request_timestamp = int(transaction_body.get("timestamp", 0))

            if abs(current_time - request_timestamp) > tolerance_seconds:
                return JsonResponse({"error": "the timestamp is expired"}, status=401)

            print("the received transaction info: ", transaction_body)

            if transaction_body.get("cause") == "transaction.confirmed":
                print("transaction confirmed! the next action will go here...")
                print("updating a customer’s invoice as paid....")

            return JsonResponse ({"status": "success"}, status = 200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status = 400)
        
    return JsonResponse({"error": "Invalid request"}, status = 400)