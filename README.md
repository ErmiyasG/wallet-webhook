# wallet-webhook
this webhook listens for events on wallet so that it automatically trigger reactions

* this webhook expected to be tested on localhost. If you're testing it from different server(IP), need to include your IP in YAYA_IPS in settings.py


* before testing the webhook, create .env file in the root directory of the app and add the signature secret key

        SIGNATURE_SECRET_KEY = "DxFWESD234sf3DE2Ngfg459Ff"

* the sample payload I used for testing(I updated the the value of 'cause' for test purpose)

        {
            "id": "1dd2854e-3a79-4548-ae36-97e4a18ebf81",
            "amount": 100,
            "currency": "ETB",
            "created_at_time": 1673381836,
            "timestamp": 1756264555,
            "cause": "transaction.confirmed",
            "full_name": "Abebe Kebede",
            "account_name": "abebekebede1",
            "invoice_url": "https://yayawallet.com/en/invoice/xxxx"
        }

* the default tolerance is 5 minutes but can be updated in settings.py

* sample curl request for test:

    curl -k -X POST http://127.0.0.1:8000/webhooks/transactions/ \
     -H "Content-Type: application/json" \
     -H "YAYA-SIGNATURE: 2b2b1ddcba77fe5e4a7c6cc272892e8c6c34f30d169f2c9c858dc5db268db069" \
     -d '{"id": "1dd2854e-3a79-4548-ae36-97e4a18ebf81","amount": 100,"currency": "ETB","created_at_time": 1673381836,"timestamp": 1756264555,"cause": "transaction.confirmed","full_name": "Abebe Kebede","account_name": "abebekebede1","invoice_url": "https://yayawallet.com/en/invoice/xxxx"}'

     
* You can generate sample YAYA-SIGNATURE for the above payload using

    echo -n "1dd2854e-3a79-4548-ae36-97e4a18ebf81100ETB16733818361756264555transaction.confirmedAbebe Kebedeabebekebede1https://yayawallet.com/en/invoice/xxxx" \
| openssl dgst -sha256 -hmac "DxFWESD234sf3DE2Ngfg459Ff"

* for the test to pass, the timestamp in the payload must be within the tolerace minute from the current time, the signed payload also need to be updated in accordance to generate a matching YAYA-SIGNATURE
