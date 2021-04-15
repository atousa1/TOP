import http.server
import socketserver
import re

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")

        self.end_headers()

        target = self.path

        pattern = r'^/user/\d+$'

        if target == '/users':

            html = f"<html><head></head><body><h1>Get ALL Users</h1></body></html>"

        elif re.match(pattern, target):

            user_id = target.split("/")[-1]

            html = f"<html><head></head><body><h1>Get User/%s</h1></body></html>" %user_id

        else:

            html = f"<html><head></head><body><h1>Atousa does not know what to do with your GET request :) </h1></body></html>"

        self.wfile.write(bytes(html, "utf8"))

        return

    def do_POST(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")

        self.end_headers()

        target = self.path

        if target == '/user':

            html = f"<html><head></head><body><h1>Create User</h1></body></html>"

        else:

            html = f"<html><head></head><body><h1>Atousa does not know what to do with your POST request :) </h1></body></html>"

        self.wfile.write(bytes(html, "utf8"))

        return

handler_object = AtousaHttpRequestHandler

PORT = 8080
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()