import http.server
import socketserver
import os
import json
import socket
import signal

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/VT323-Regular.ttf':
            try:
                with open('VT323-Regular.ttf', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'font/ttf')
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except: pass
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode())

    def do_POST(self):
        if self.path != '/upload': return
        try:
            content_length = int(self.headers['Content-Length'])
            boundary = self.headers['Content-Type'].split('=')[1].encode()
            remainbytes = content_length
            line = self.rfile.readline()
            remainbytes -= len(line)
            if not boundary in line: return
            upload_dir = 'DataCore'
            os.makedirs(upload_dir, exist_ok=True)
            line = self.rfile.readline()
            remainbytes -= len(line)
            filename = line.decode()
            if "filename=" in filename:
                filename = filename.split('filename=')[1].strip().strip('"')
                filepath = os.path.join(upload_dir, filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                line = self.rfile.readline()
                remainbytes -= len(line)
                line = self.rfile.readline()
                remainbytes -= len(line)
                with open(filepath, 'wb') as out:
                    preline = self.rfile.readline()
                    remainbytes -= len(preline)
                    while remainbytes > 0:
                        line = self.rfile.readline()
                        remainbytes -= len(line)
                        if boundary in line:
                            preline = preline[0:-1]
                            if preline.endswith(b'\r'): preline = preline[0:-1]
                            out.write(preline)
                            break
                        else:
                            out.write(preline)
                            preline = line
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                return
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())

HTML_TEMPLATE = """
<!DOCTYPE html><html><head><title>NIGHT CITY DATALINK</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>
@font-face{font-family:'VT323';src:url('VT323-Regular.ttf') format('truetype')}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'VT323',monospace;background-color:#0a0a0a;color:#f0f;line-height:1.4;padding:20px;background-image:linear-gradient(45deg,#0a0a0a 25%,#0f0f0f 25%,#0f0f0f 50%,#0a0a0a 50%,#0a0a0a 75%,#0f0f0f 75%,#0f0f0f);background-size:20px 20px}
.container{max-width:1200px;margin:0 auto;width:100%;position:relative}
.header{text-align:center;margin-bottom:30px;text-shadow:0 0 10px #f0f}
.title{font-size:48px;margin:20px 0;letter-spacing:4px;animation:glitch 1s infinite}
.subtitle{color:#666;margin-bottom:20px;text-transform:uppercase}
.main-section{background-color:rgba(17,17,17,0.9);padding:20px;margin-bottom:20px;border:1px solid #f0f;box-shadow:0 0 20px rgba(255,0,255,0.2)}
.hack-btn{background-color:#1a1a1a;border:1px solid #f0f;color:#f0f;font-family:'VT323',monospace;font-size:24px;padding:15px 40px;cursor:pointer;width:100%;max-width:300px;margin:20px auto;display:block;letter-spacing:2px;text-transform:uppercase;transition:all 0.3s}
.hack-btn:hover{background-color:#f0f;color:#000;box-shadow:0 0 20px #f0f}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:20px 0}
.stat-box{background-color:rgba(26,26,26,0.9);padding:10px;border:1px solid #f0f}
.progress-container{margin:20px 0}
.progress-bar{width:100%;height:30px;background-color:rgba(26,26,26,0.9);border:1px solid #f0f;position:relative}
.progress{width:0%;height:100%;background:linear-gradient(90deg,#f0f,#0ff);transition:width .3s ease-in-out}
.status-text{position:absolute;width:100%;text-align:center;top:50%;transform:translateY(-50%);color:#fff;font-size:16px;text-shadow:0 0 5px #f0f}
.log-container{height:200px;overflow-y:auto;background-color:rgba(26,26,26,0.9);padding:10px;border:1px solid #f0f;font-size:14px;margin-top:20px}
.log-entry{border-bottom:1px solid #f0f;padding:5px 0;color:#0ff}
.log-time{color:#f0f}
#file-input{display:none}
.footer{text-align:center;color:#f0f;margin-top:20px;font-size:14px;text-shadow:0 0 5px #f0f}
@keyframes glitch{0%{text-shadow:2px 2px #f0f,-2px -2px #0ff}50%{text-shadow:-2px 2px #f0f,2px -2px #0ff}100%{text-shadow:2px -2px #f0f,-2px 2px #0ff}}
@media (max-width:768px){.title{font-size:32px}.stats-grid{grid-template-columns:1fr}}
</style></head><body><div class="container">
<div class="header"><div class="subtitle">NIGHT CITY SECURE DATA EXTRACTION v2.0.7.7</div></div>
<div class="main-section">
<div class="stats-grid">
<div class="stat-box"><div>STATUS: <span id="status">READY</span></div></div>
<div class="stat-box"><div>FILES DETECTED: <span id="files-count">0</span></div></div>
<div class="stat-box"><div>DATA TRANSFERRED: <span id="data-size">0 MB</span></div></div>
<div class="stat-box"><div>SPEED: <span id="speed">0 MB/s</span></div></div>
</div>
<input type="file" id="file-input" multiple>
<button class="hack-btn" onclick="startHack()">JACK IN</button>
<div class="progress-container">
<div class="progress-bar">
<div class="progress"></div>
<div class="status-text">WAITING FOR NEURAL LINK</div>
</div></div>
<div class="log-container" id="log"></div></div>
<div class="footer">CREATED BY THERASPUTIN64 | NIGHT CITY NETWORKS</div></div>
<script>
const l=document.getElementById('log'),p=document.querySelector('.progress'),s=document.querySelector('.status-text'),f=document.getElementById('file-input');let t=0,u=0,d=0;
function a(m){const t=new Date().toLocaleTimeString(),e=document.createElement('div');e.className='log-entry';e.innerHTML=`<span class="log-time">[${t}]</span> ${m}`;l.appendChild(e);l.scrollTop=l.scrollHeight}
function startHack(){document.getElementById('status').textContent='SCANNING';a('INITIATING NEURAL LINK...');f.click()}
f.addEventListener('change',async function(){const files=Array.from(this.files);t=files.length;u=0;d=0;document.getElementById('files-count').textContent=t;document.getElementById('status').textContent='EXTRACTING';a(`DETECTED ${t} FILES IN THE MAINFRAME`);for(const file of files){const fd=new FormData();fd.append('file',file);try{const st=Date.now(),x=new XMLHttpRequest();x.upload.addEventListener('progress',function(e){if(e.lengthComputable){const pc=((u/t)*100)+((e.loaded/e.total)*(100/t));p.style.width=pc+'%';const et=(Date.now()-st)/1000,us=(e.loaded/et/(1024*1024)).toFixed(2);document.getElementById('speed').textContent=`${us} MB/s`;s.textContent=`EXTRACTING: ${Math.round(pc)}%`}});x.onload=function(){if(x.status===200){u++;d+=file.size/(1024*1024);document.getElementById('data-size').textContent=`${d.toFixed(2)} MB`;a(`EXTRACTED: ${file.name}`);if(u===t){document.getElementById('status').textContent='MISSION COMPLETE';s.textContent='DATA EXTRACTION SUCCESSFUL';a('ALL FILES SECURED - NEURAL LINK STABLE')}}else{a(`EXTRACTION FAILED: ${file.name}`)}};x.onerror=function(){a(`NEURAL LINK ERROR: ${file.name}`)};x.open('POST','/upload',true);x.send(fd)}catch(e){a(`SYSTEM FAILURE: ${e}`)}}});
</script></body></html>
"""

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

def signal_handler(sig, frame):
    print("\n[!] NEURAL LINK TERMINATED - CLOSING SECURE CONNECTION...")
    os._exit(0)

if __name__ == '__main__':
    PORT = 8080
    signal.signal(signal.SIGINT, signal_handler)
    
    print("""
    \033[35m
    ███▄    █ ▓█████▄▄▄█████▓ ██▀███   █    ██  ███▄    █  ███▄    █ ▓█████  ██▀███  
    ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓██ ▒ ██▒ ██  ▓██▒ ██ ▀█   █  ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒
   ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▓██ ░▄█ ▒▓██  ▒██░▓██  ▀█ ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒
   ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ▒██▀▀█▄  ▓▓█  ░██░▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄  
   ▒██░   ▓██░▒████▒  ▒██▒ ░ ░██▓ ▒██▒▒▒█████▓ ▒██░   ▓██░▒██░   ▓██░░████▒ ░██▓ ▒██▒
    \033[0m
    """)
    
    print("\033[35m[*] INITIALIZING SECURE DATA TRANSFER PROTOCOL...")
    with socketserver.TCPServer(("", PORT), UploadHandler) as httpd:
        host = get_local_ip()
        print(f"[+] NEURAL LINK ESTABLISHED - PORT {PORT}")
        print(f"[+] ACCESS CODE: http://{host}:{PORT}")
        print("[+] DATACORE ACCESS INITIALIZED")
        print("[!] PRESS CTRL+C TO TERMINATE NEURAL LINK")
        try: os.startfile('DataCore')
        except: pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
