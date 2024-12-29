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
            except:
                pass
        elif self.path == '/link.ico':
            try:
                with open('link.ico', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/x-icon')
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except:
                pass
        elif self.path == '/favicon.ico':  # Also handle standard favicon.ico requests
            try:
                with open('link.ico', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/x-icon')
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            except:
                pass
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
<!DOCTYPE html><html><head><title>DATALINK</title><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="link.ico" type="image/x-icon"><style>
@font-face{font-family:'VT323';src:url('VT323-Regular.ttf') format('truetype')}
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden}
body{font-family:'VT323',monospace;background:#0a0a0a;color:#00ff8c;display:flex;flex-direction:column}
.container{height:100vh;display:flex;flex-direction:column;padding:1vh}
.header{flex:0 0 12vh;display:flex;flex-direction:column;justify-content:center;align-items:center;background:rgba(0,0,0,0.7);border-left:4px solid #00ff8c;border-right:4px solid #00ff8c;padding:1vh;position:relative;overflow:hidden}
.header::before{content:'';position:absolute;top:0;left:-5%;width:110%;height:100%;background:rgba(0,255,140,0.1);transform:skewX(-20deg);animation:scanline 4s linear infinite}
.title{font-size:clamp(2rem,6vw,4.5rem);letter-spacing:0.3em;text-transform:uppercase;position:relative;text-align:center}
.glitch-wrapper{position:relative}
.glitch-text{animation:mainGlitch 3s infinite}
.glitch-text::before,.glitch-text::after{content:'DATALINK';position:absolute;top:0;width:100%;height:100%;left:0}
.glitch-text::before{color:#ff0080;animation:glitch 4s infinite;clip-path:polygon(0 0,100% 0,100% 45%,0 45%);transform:translate(-0.025em,0.0125em);opacity:0.75}
.glitch-text::after{color:#0ff;animation:glitch 4s infinite;clip-path:polygon(0 80%,100% 20%,100% 100%,0 100%);transform:translate(0.025em,-0.0125em);opacity:0.75}
.subtitle{font-size:clamp(1rem,2vw,1.5rem);text-transform:uppercase;letter-spacing:0.4em;color:#00ccff;text-align:center;margin-top:1vh}
.main-section{flex:1;display:flex;flex-direction:column;gap:1vh;background:rgba(0,0,0,0.8);border-left:4px solid #00ff8c;border-right:4px solid #00ff8c;margin:1vh 0;padding:1vh}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1vh;flex:0 0 auto}
.stat-box{background:rgba(0,255,140,0.1);border:2px solid #00ff8c;padding:1vh;display:flex;align-items:center}
.stat-box div{font-size:clamp(0.9rem,1.8vw,1.4rem);letter-spacing:0.1em}
.hack-btn{background:#111;border:4px solid #00ff8c;color:#00ff8c;font-family:'VT323',monospace;font-size:clamp(2rem,5vw,4rem);cursor:pointer;width:100%;margin:1vh 0;padding:2vh;display:flex;align-items:center;justify-content:center;letter-spacing:0.3em;text-transform:uppercase;transition:all 0.2s;flex:0 0 auto;min-height:10vh}
.hack-btn:hover{background:#00ff8c;color:#000}
.progress-container{flex:0 0 6vh;margin:1vh 0}
.progress-bar{width:100%;height:100%;background:rgba(0,0,0,0.8);border:2px solid #00ff8c;position:relative;overflow:hidden}
.progress{width:0%;height:100%;background:#00ff8c;transition:width .3s ease-in-out}
.status-text{position:absolute;width:100%;text-align:center;top:50%;transform:translateY(-50%);mix-blend-mode:difference;color:#fff;font-size:clamp(0.9rem,2vw,1.4rem);letter-spacing:0.2em}
.log-container{flex:1;min-height:0;max-height:250px; background:rgba(0,0,0,0.8);border:2px solid #00ff8c;padding:1vh;font-size:clamp(0.8rem,1.6vw,1.2rem);overflow-y:auto}
.log-entry{border-bottom:1px solid #00ff8c;padding:0.5vh 0;color:#00ccff}
.log-time{color:#00ff8c}
#file-input{display:none}
.footer{flex:0 0 5vh;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);border-left:4px solid #00ff8c;border-right:4px solid #00ff8c;color:#00ff8c;font-size:clamp(0.7rem,1.4vw,1rem);letter-spacing:0.2em}
@keyframes scanline{0%{transform:translateY(-100%) skewX(-20deg)}100%{transform:translateY(200%) skewX(-20deg)}}
@keyframes mainGlitch{0%,100%{opacity:1}35%,65%{opacity:0.95}36%,64%{opacity:1}37%,63%{opacity:0.95}}
@keyframes glitch{0%{clip-path:inset(40% 0 61% 0)}20%{clip-path:inset(92% 0 1% 0)}40%{clip-path:inset(43% 0 1% 0)}60%{clip-path:inset(25% 0 58% 0)}80%{clip-path:inset(54% 0 7% 0)}100%{clip-path:inset(58% 0 43% 0)}}
</style></head><body><div class="container">
<div class="header">
<div class="glitch-wrapper">
<h1 class="title glitch-text">DATALINK</h1>
</div>
<div class="subtitle">NEURAL INTERFACE READY</div>
</div>
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
<div class="log-container" id="log"></div>
</div>
<div class="footer">CREATED BY THERASPUTIN64 | NIGHT CITY NETWORKS</div>
</div>
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
    PORT = 8081
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