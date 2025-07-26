import http.server
import socketserver
import os
import sys

PORT = 12001
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         "static/frontend/reddit-app/dist")

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        # Redirect root to /django_reddit/
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/django_reddit/')
            self.end_headers()
            return
        
        # Handle /django_reddit/ path
        if self.path.startswith('/django_reddit/'):
            # Check for specific files first
            if self.path == '/django_reddit/styles.css':
                self.path = '/styles.css'
            elif self.path == '/django_reddit/runtime.js':
                self.path = '/runtime.js'
            elif self.path == '/django_reddit/polyfills.js':
                self.path = '/polyfills.js'
            elif self.path == '/django_reddit/main.js':
                self.path = '/main.js'
            elif self.path.startswith('/django_reddit/assets/'):
                self.path = self.path.replace('/django_reddit/assets/', '/assets/')
            else:
                # For SPA routing, serve index.html for paths that don't match files
                file_path = os.path.join(DIRECTORY, self.path[len('/django_reddit/'):])
                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    self.path = '/index.html'
                else:
                    # Remove the /django_reddit/ prefix for direct file access
                    self.path = self.path[len('/django_reddit/'):]
        
        return super().do_GET()

if __name__ == "__main__":
    print(f"Serving at http://0.0.0.0:{PORT}")
    print(f"Serving directory: {DIRECTORY}")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), CORSHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)