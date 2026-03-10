#!/usr/bin/env python3
# setup.py - Auto setup script

import os
import subprocess
import threading
import time
import socket
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>🔥 RAILWAY RDP 🔥</title>
                <style>
                    body { background: #0a0a0a; color: #00ff00; font-family: monospace; padding: 20px; }
                    .container { max-width: 800px; margin: 0 auto; border: 2px solid #00ff00; padding: 20px; }
                    h1 { color: #00ff00; text-align: center; }
                    .info { margin: 20px 0; padding: 10px; border: 1px solid #00ff00; }
                    .success { color: #00ff00; }
                    .cmd { background: #1a1a1a; padding: 10px; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔥 RAILWAY RDP SERVER 🔥</h1>
                    <div class="info">
                        <h2>📊 STATUS</h2>
                        <p class="success">✅ Server Running</p>
                        <p>🆙 Uptime: <span id="uptime">Calculating...</span></p>
                        <p>💾 Memory: <span id="memory">Loading...</span></p>
                        <p>💽 Disk: <span id="disk">Loading...</span></p>
                    </div>
                    
                    <div class="info">
                        <h2>🔗 CONNECTION DETAILS</h2>
                        <h3>RDP Direct:</h3>
                        <div class="cmd">Host: {host}<br>Port: 3389<br>User: root<br>Pass: Antyrx@123</div>
                        
                        <h3>Web VNC:</h3>
                        <div class="cmd"><a href="/vnc.html" style="color:#00ff00;">Click here for Web VNC</a></div>
                        
                        <h3>File Access:</h3>
                        <div class="cmd">http://{host}:8000/files/</div>
                    </div>
                    
                    <div class="info">
                        <h2>📁 FILES</h2>
                        <div id="filelist">Loading files...</div>
                    </div>
                </div>
                
                <script>
                    function updateStats() {{
                        fetch('/stats').then(r=>r.json()).then(data => {{
                            document.getElementById('uptime').innerText = data.uptime;
                            document.getElementById('memory').innerText = data.memory;
                            document.getElementById('disk').innerText = data.disk;
                        }});
                        
                        fetch('/files').then(r=>r.json()).then(data => {{
                            let html = '<ul>';
                            data.files.forEach(f => {{
                                html += `<li><a href="/files/${{f}}" style="color:#00ff00;">${{f}}</a></li>`;
                            }});
                            html += '</ul>';
                            document.getElementById('filelist').innerHTML = html;
                        }});
                    }}
                    
                    updateStats();
                    setInterval(updateStats, 5000);
                </script>
            </body>
            </html>
            """.format(host=socket.gethostname())
            
            self.wfile.write(html.encode())
        elif self.path == '/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            uptime = os.popen("uptime").read().strip()
            memory = os.popen("free -h | grep Mem").read().strip()
            disk = os.popen("df -h /").read().strip()
            
            stats = {
                "uptime": uptime,
                "memory": memory,
                "disk": disk
            }
            
            self.wfile.write(json.dumps(stats).encode())
        elif self.path == '/files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            files = os.listdir('/root')
            self.wfile.write(json.dumps({"files": files}).encode())
        else:
            super().do_GET()

def start_file_server():
    """Start file server"""
    os.chdir('/root')
    handler = CustomHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print(f"🌐 File server running on port 8000")
        httpd.serve_forever()

def monitor_system():
    """Monitor system resources"""
    while True:
        cpu = os.popen("top -bn1 | grep 'Cpu(s)'").read().strip()
        mem = os.popen("free -h | grep Mem").read().strip()
        
        print(f"\n📊 System Status @ {time.ctime()}")
        print(f"CPU: {cpu}")
        print(f"Memory: {mem}")
        print("-" * 50)
        
        time.sleep(60)

def setup_nginx():
    """Setup nginx reverse proxy"""
    os.system("service nginx start")

def main():
    print("🔥 Railway RDP Setup Starting...")
    
    # Start threads
    threading.Thread(target=start_file_server, daemon=True).start()
    threading.Thread(target=monitor_system, daemon=True).start()
    threading.Thread(target=setup_nginx, daemon=True).start()
    
    # Keep main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()