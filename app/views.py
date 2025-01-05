import json
import requests
from django.shortcuts import render

def api_tester(request):
    response_data = None
    if request.method == "POST":
        url = request.POST.get("url")
        method = request.POST.get("method")
        headers = request.POST.get("headers", "{}")
        body = request.POST.get("body", "{}")

        try:
            headers = json.loads(headers) if headers else {}
            body = json.loads(body) if body else {}

            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=body)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=body)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)

            response_data = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text,
            }
        except Exception as e:
            response_data = {"error": str(e)}

    return render(request, "app/index.html", {"response": json.dumps(response_data, indent=4) if response_data else None})
