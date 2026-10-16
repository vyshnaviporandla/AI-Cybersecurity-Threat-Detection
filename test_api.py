import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:5001"

def test_request(name, payload):
    print(f"\n--- {name} ---")
    request = urllib.request.Request(
        BASE_URL + "/api/predict",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            print("HTTP status:", response.status)
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print("HTTP status:", error.code)
        print(error.read().decode("utf-8"))

test_request("Missing features", {"features": {}})

with urllib.request.urlopen(BASE_URL + "/api/sample") as response:
    sample = json.loads(response.read().decode("utf-8"))

sample["features"]["ackdat"] = "not-a-number"
test_request("Invalid numeric value", sample)