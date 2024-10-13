import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleAPIHandler(BaseHTTPRequestHandler):

    # Handle GET requests
    def do_GET(self):
        if self.path == '/greet':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'API Server works, Hi professor!'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found!')

    # Handle POST requests
    def do_POST(self):
        if self.path == '/data':
            content_length = int(self.headers['Content-Length'])  # Get the size of the data
            post_data = self.rfile.read(content_length)  # Get the actual data
            try:
                # Parse the received JSON data
                received_data = json.loads(post_data)
                message = received_data.get('message', 'No message provided')

                # Send response back
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'response': f'Received your message: {message}'}
                self.wfile.write(json.dumps(response).encode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON format!')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Endpoint not found!')

def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
