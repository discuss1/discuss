import http.server
import socketserver
import os
import sys
import mimetypes
import urllib.parse

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
        # Prevent downloads by ensuring proper content-type
        self.send_header('X-Content-Type-Options', 'nosniff')
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
            
            # If empty path or ends with /, serve index.html
            if not clean_path or clean_path.endswith('/'):
                print(f"Serving index.html for path: {self.path}")
                self.serve_index_html()
                return
            
            # If it's a specific file, serve it
            file_path = os.path.join(DIRECTORY, clean_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                print(f"Serving file: {file_path}")
                self.serve_file(clean_path)
                return
            else:
                # For SPA routing, serve index.html
                print(f"File not found, serving index.html for SPA routing: {self.path}")
                self.serve_index_html()
                return
        
        # Default handling
        try:
            return super().do_GET()
        except Exception as e:
            print(f"Error serving {self.path}: {str(e)}")
            self.send_error(500, f"Server Error: {str(e)}")
    
    def serve_index_html(self):
        """Serve the index.html file with proper content type"""
        index_path = os.path.join(DIRECTORY, 'index.html')
        try:
            with open(index_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"Error serving index.html: {str(e)}")
            self.send_error(500, f"Error serving index.html: {str(e)}")
    
    def serve_file(self, file_path):
        """Serve a specific file with proper content type"""
        full_path = os.path.join(DIRECTORY, file_path)
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(full_path)
            if not content_type:
                if file_path.endswith('.js'):
                    content_type = 'application/javascript'
                elif file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.html'):
                    content_type = 'text/html; charset=utf-8'
                else:
                    content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"Error serving file {file_path}: {str(e)}")
            self.send_error(404, f"File not found: {file_path}")
            
    def guess_type(self, path):
        """Guess the type of a file based on its extension."""
        content_type, _ = mimetypes.guess_type(path)
        if content_type:
            return content_type
        
        # Fallback for common web files
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.css'):
            return 'text/css'
        elif path.endswith('.html'):
            return 'text/html; charset=utf-8'
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