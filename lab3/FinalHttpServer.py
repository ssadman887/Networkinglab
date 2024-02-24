import http.server
from socketserver import ThreadingMixIn
import socketserver
import os

class ThreadedHTTPServer(ThreadingMixIn, socketserver.TCPServer):
    """Handle requests in a separate thread."""

class CustomRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS header to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_POST(self):
        # Handle file upload
        content_length = int(self.headers['Content-Length'])
        file_data = self.rfile.read(content_length)

        # Assuming the client sends the file name in the 'Filename' header
        # You may need to adjust this if using a different header or method
        filename = self.headers.get('Filename')
        if not filename:
            # Respond with an error if the filename is not provided
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Filename header missing")
            return

        # Save the file with the provided name
        path = os.path.join(os.getcwd(), filename)
        with open(path, 'wb') as file:
            file.write(file_data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"File uploaded successfully.")

    def do_GET(self):
        # Override to handle file download requests
        super().do_GET()

# Set the port for the HTTP server
port = 8080

# Create an HTTP server with the custom request handler
with ThreadedHTTPServer(('', port), CustomRequestHandler) as httpd:
    print(f"Serving files on port {port}...")
    httpd.serve_forever()