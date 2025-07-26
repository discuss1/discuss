import http.server
import socketserver
import os
import sys
import subprocess
import signal
import time
import urllib.request
import urllib.error
import threading

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

# Function to print Django output
def print_django_output():
    for line in iter(django_process.stdout.readline, ''):
        print(f"Django: {line.strip()}")

# Start thread to print Django output
threading.Thread(target=print_django_output, daemon=True).start()

# Give Django time to start
time.sleep(3)
print("Django server should be running now")

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")
    
    def add_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
    
    def do_HEAD(self):
        self.do_GET(body=False)
        
    def do_GET(self, body=True):
        # Forward the request to Django
        url = f'http://localhost:{DJANGO_PORT}{self.path}'
        print(f"Proxying GET request to: {url}")
        
        try:
            req = urllib.request.Request(url, method='GET')
            # Copy headers from client request to Django request
            for header in self.headers:
                if header.lower() not in ('host', 'connection'):
                    req.add_header(header, self.headers[header])
                    
            response = urllib.request.urlopen(req)
            
            # Copy response status
            self.send_response(response.status)
            
            # Add CORS headers
            self.add_cors_headers()
            
            # Copy response headers
            for header in response.headers:
                if header.lower() not in ('server', 'date', 'connection'):
                    self.send_header(header, response.headers[header])
                    
            self.end_headers()
            
            # Copy response body
            if body:
                response_data = response.read()
                self.wfile.write(response_data)
                print(f"Sent {len(response_data)} bytes in response")
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            self.send_response(e.code)
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"Error in GET: {str(e)}")
            self.send_response(502)  # Bad Gateway
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else None
        
        # Forward the request to Django
        url = f'http://localhost:{DJANGO_PORT}{self.path}'
        print(f"Proxying POST request to: {url}")
        
        try:
            headers = {}
            # Copy headers from client request to Django request
            for header in self.headers:
                if header.lower() not in ('host', 'connection'):
                    headers[header] = self.headers[header]
                    
            req = urllib.request.Request(url, data=post_data, headers=headers, method='POST')
            response = urllib.request.urlopen(req)
            
            # Copy response status
            self.send_response(response.status)
            
            # Add CORS headers
            self.add_cors_headers()
            
            # Copy response headers
            for header in response.headers:
                if header.lower() not in ('server', 'date', 'connection'):
                    self.send_header(header, response.headers[header])
                    
            self.end_headers()
            
            # Copy response body
            response_data = response.read()
            self.wfile.write(response_data)
            print(f"Sent {len(response_data)} bytes in response")
            
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            self.send_response(e.code)
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"Error in POST: {str(e)}")
            self.send_response(502)  # Bad Gateway
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())
    
    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        put_data = self.rfile.read(content_length) if content_length > 0 else None
        
        # Forward the request to Django
        url = f'http://localhost:{DJANGO_PORT}{self.path}'
        print(f"Proxying PUT request to: {url}")
        
        try:
            headers = {}
            # Copy headers from client request to Django request
            for header in self.headers:
                if header.lower() not in ('host', 'connection'):
                    headers[header] = self.headers[header]
                    
            req = urllib.request.Request(url, data=put_data, headers=headers, method='PUT')
            response = urllib.request.urlopen(req)
            
            # Copy response status
            self.send_response(response.status)
            
            # Add CORS headers
            self.add_cors_headers()
            
            # Copy response headers
            for header in response.headers:
                if header.lower() not in ('server', 'date', 'connection'):
                    self.send_header(header, response.headers[header])
                    
            self.end_headers()
            
            # Copy response body
            response_data = response.read()
            self.wfile.write(response_data)
            print(f"Sent {len(response_data)} bytes in response")
            
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            self.send_response(e.code)
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"Error in PUT: {str(e)}")
            self.send_response(502)  # Bad Gateway
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())
        
    def do_DELETE(self):
        # Forward the request to Django
        url = f'http://localhost:{DJANGO_PORT}{self.path}'
        print(f"Proxying DELETE request to: {url}")
        
        try:
            headers = {}
            # Copy headers from client request to Django request
            for header in self.headers:
                if header.lower() not in ('host', 'connection'):
                    headers[header] = self.headers[header]
                    
            req = urllib.request.Request(url, headers=headers, method='DELETE')
            response = urllib.request.urlopen(req)
            
            # Copy response status
            self.send_response(response.status)
            
            # Add CORS headers
            self.add_cors_headers()
            
            # Copy response headers
            for header in response.headers:
                if header.lower() not in ('server', 'date', 'connection'):
                    self.send_header(header, response.headers[header])
                    
            self.end_headers()
            
            # Copy response body
            response_data = response.read()
            self.wfile.write(response_data)
            print(f"Sent {len(response_data)} bytes in response")
            
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
            self.send_response(e.code)
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"Error in DELETE: {str(e)}")
            self.send_response(502)  # Bad Gateway
            self.add_cors_headers()
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.add_cors_headers()
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