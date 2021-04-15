import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")

        self.end_headers()

        html = f"<html><head></head><body><h1>Hello World!</h1></body></html>"

        self.wfile.write(bytes(html, "utf8"))

        return

handler_object = AtousaHttpRequestHandler

PORT = 9090
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()