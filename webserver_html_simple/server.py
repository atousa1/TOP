import http.server
import socketserver
import re
import os

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")
        
        self.end_headers()

        htmlFilePath = os.getcwd() + "/webserver_html_simple/index.html"

        with open(htmlFilePath, 'rb') as fin:
            self.copyfile(fin, self.wfile)

        return

handler = AtousaHttpRequestHandler

PORT = 9091
my_server = socketserver.TCPServer(("", PORT), handler)

my_server.serve_forever()