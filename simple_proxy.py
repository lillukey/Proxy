import http.server
import urllib.request

class SimpleProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the incoming request URL
        print(f"Proxying request for: {self.path}")
        
        try:
            # Forward the request to the destination website
            req = urllib.request.Request(self.path, headers=self.headers)
            with urllib.request.urlopen(req) as response:
                # Send the response back to the client browser
                self.send_response(response.status)
                for key, value in response.getheaders():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_error(500, f"Proxy Error: {e}")

if __name__ == "__main__":
    # Start the proxy server locally on port 8080
    server_address = ('127.0.0.1', 8080)
    httpd = http.server.HTTPServer(server_address, SimpleProxyHandler)
    print("Local proxy running on http://127.0.0.1:8080")
    httpd.serve_forever()
