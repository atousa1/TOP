import http.server
import socketserver
import re

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")
        # self.send_header('location', 'index.html')  
        self.end_headers()

        with open('index.html', 'rb') as fin:
            self.copyfile(fin, self.wfile)

        return

handler_object = AtousaHttpRequestHandler

PORT = 7070
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()