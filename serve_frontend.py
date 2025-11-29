import http.server
import socketserver
import os
import sys
import mimetypes

PORT = 12001
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         "static/frontend/reddit-app/dist")

# Ensure all common MIME types are registered
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('image/png', '.png')
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('image/jpeg', '.jpeg')
mimetypes.add_type('image/gif', '.gif')
mimetypes.add_type('font/woff', '.woff')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('font/ttf', '.ttf')

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
        
    def do_GET(self):
        print(f"GET request for: {self.path}")
        
        # Redirect root to /django_reddit/
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/django_reddit/')
            self.end_headers()
            return
        
        # Handle /django_reddit/ path
        if self.path.startswith('/django_reddit/'):
            # Strip the /django_reddit/ prefix for all files
            clean_path = self.path[len('/django_reddit/'):]
            
            # If it's a specific file, serve it
            file_path = os.path.join(DIRECTORY, clean_path)
            if clean_path and os.path.exists(file_path) and os.path.isfile(file_path):
                print(f"Serving file: {file_path}")
                self.path = '/' + clean_path
            else:
                # For SPA routing, serve index.html
                print(f"File not found, serving index.html for SPA routing: {self.path}")
                self.path = '/index.html'
        
        try:
            return super().do_GET()
        except Exception as e:
            print(f"Error serving {self.path}: {str(e)}")
            self.send_error(500, f"Server Error: {str(e)}")
            
    def guess_type(self, path):
        """Guess the type of a file based on its extension."""
        base, ext = os.path.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return 'application/octet-stream'

if __name__ == "__main__":
    print(f"Serving at http://0.0.0.0:{PORT}")
    print(f"Serving directory: {DIRECTORY}")
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), CORSHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)