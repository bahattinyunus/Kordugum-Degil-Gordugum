#!/usr/bin/env python3
"""
Gönül Portalı Yerel Sunucusu (Local Web Server).
Tek bir komutla web portalını yerel tarayıcınızda başlatır.
Kullanım: python web/serve.py [port]
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        # Temiz ve sade terminal günlüğü
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

if __name__ == "__main__":
    print(f"\n🕊️  Kördüğüm Değil Gördüğüm — Web Portalı Başlatılıyor...")
    print(f"👉 Adres: http://localhost:{PORT}")
    print("Çıkmak için CTRL+C tuşlarına basabilirsiniz.\n")

    try:
        with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
            try:
                webbrowser.open(f"http://localhost:{PORT}")
            except Exception:
                pass
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatıldı. Sevgiyle kalın!")
