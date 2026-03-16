import json
import urllib.request

url = "http://localhost:8000/predict"

sample = {
    "step": 1,
    "type": "TRANSFER",
    "amount": 1000.0,
    "nameOrig": "C123",
    "oldbalanceOrg": 5000.0,
    "newbalanceOrig": 4000.0,
    "nameDest": "C456",
    "oldbalanceDest": 0.0,
    "newbalanceDest": 0.0
}

data = json.dumps(sample).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        print("Status:", resp.status)
        print(resp.read().decode())
except Exception as e:
    print("Request failed:", repr(e))
