import os
import json

APK_DIR = os.path.join(os.path.dirname(__file__), "apks")

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    
    if path == "/api/apps":
        apps = []
        for i, filename in enumerate(os.listdir(APK_DIR)):
            if filename.endswith(".apk"):
                apps.append({
                    "id": i + 1,
                    "name": filename,
                    "package": filename[:-4],
                    "url": f"/apks/{filename}",
                })
        data = json.dumps(apps).encode()
        start_response("200 OK", [("Content-Type", "application/json")])
        return [data]
    
    elif path.startswith("/apks/"):
        filename = path.replace("/apks/", "")
        filepath = os.path.join(APK_DIR, filename)
        if os.path.exists(filepath):
            start_response("200 OK", [("Content-Type", "application/vnd.android.package-archive")])
            with open(filepath, "rb") as f:
                return [f.read()]
    
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not Found"]
