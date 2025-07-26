import http.server
import socketserver
import os
import sys
import subprocess
import signal
import time

PORT = 12000
DJANGO_PORT = 8000

# Start Django server
django_process = subprocess.Popen(
    ["python", "manage.py", "runserver", f"0.0.0.0:{DJANGO_PORT}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1
)

# Give Django time to start
time.sleep(2)

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET(body=False)
        
    def do_GET(self, body=True):
        import urllib.request
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
        
        # Forward the request to Django
        url = f'http://localhost:{DJANGO_PORT}{self.path}'
        
        try:
            response = urllib.request.urlopen(url)
            
            # Copy response headers
            for header in response.headers:
                self.send_header(header, response.headers[header])
                
            self.end_headers()
            
            # Copy response body
            if body:
                self.wfile.write(response.read())
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
    
    def do_POST(self):
        import urllib.request
        import urllib.error
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Forward the request to Django
        url = f'http://localhost:{DJANGO_PORT}{self.path}'
        
        try:
            headers = {k: v for k, v in self.headers.items()}
            req = urllib.request.Request(url, data=post_data, headers=headers, method='POST')
            response = urllib.request.urlopen(req)
            
            # Copy response status and headers
            self.send_response(response.status)
            
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
            
            for header in response.headers:
                self.send_header(header, response.headers[header])
                
            self.end_headers()
            
            # Copy response body
            self.wfile.write(response.read())
            
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
    
    def do_PUT(self):
        self.do_POST()
        
    def do_DELETE(self):
        self.do_POST()
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
        self.end_headers()

if __name__ == "__main__":
    print(f"Starting proxy server at http://0.0.0.0:{PORT}")
    print(f"Forwarding to Django at http://localhost:{DJANGO_PORT}")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        # Kill Django process
        django_process.terminate()
        django_process.wait()
        print("Django server stopped.")
        sys.exit(0)