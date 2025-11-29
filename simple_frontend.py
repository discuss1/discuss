#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

PORT = 12001
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         "static/frontend/reddit-app/dist")

class SPAHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
        super().end_headers()

    def do_GET(self):
        # Handle root redirect
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/django_reddit/')
            self.end_headers()
            return
        
        # Handle /django_reddit/ paths
        if self.path.startswith('/django_reddit/'):
            # Remove the /django_reddit/ prefix
            clean_path = self.path[len('/django_reddit/'):]
            
            # If it's empty or a directory, serve index.html
            if not clean_path or clean_path.endswith('/'):
                self.path = '/index.html'
            else:
                # Check if the file exists
                file_path = os.path.join(DIRECTORY, clean_path)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    self.path = '/' + clean_path
                else:
                    # For SPA routing, serve index.html
                    self.path = '/index.html'
        
        return super().do_GET()

if __name__ == "__main__":
    print(f"Starting server at http://0.0.0.0:{PORT}")
    print(f"Serving directory: {DIRECTORY}")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), SPAHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")