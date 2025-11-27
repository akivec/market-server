import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

APK_DIR = "/apks"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/apps":
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
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)
            return

        if self.path.startswith("/apks/"):
            filename = self.path.replace("/apks/", "")
            filepath = os.path.join(APK_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
                return

        self.send_response(404)
        self.end_headers()
