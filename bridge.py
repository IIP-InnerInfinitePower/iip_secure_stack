import os

API_KEY = os.getenv("API_KEY", "")

async def app(scope, receive, send):
    if scope.get("type") != "http":
        await send({"type": "http.response.start", "status": 500, "headers": []})
        await send({"type": "http.response.body", "body": b""})
        return

    path = scope.get("path", "/")
    method = scope.get("method", "GET").upper()

    if method == "GET" and path in ("/", "/health", "/healthz"):
        body = b'{"status":"ok"}'
        headers = [(b"content-type", b"application/json")]
        await send({"type": "http.response.start", "status": 200, "headers": headers})
        await send({"type": "http.response.body", "body": body})
    else:
        await send({"type": "http.response.start", "status": 404,
                    "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": b'{"detail":"Not Found"}'})
