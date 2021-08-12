import http.server
import socketserver
import re
import os
from sys import platform

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")
        
        self.end_headers()
        target = self.path
        pattern_file = r'^/[\w+]\.[\w+]$'
        pattern_folder = r'^/[\w+]/[\w+]\.[\w+]$'

        if re.match(pattern_file, target):

            # if platform.startswith("linux"):
            #     htmlFilePath = os.getcwd() + "/ajax_submission/webserver_html_simple/user.html"
            # elif platform.startswith("win32"):
            htmlFilePath = os.getcwd() + "/ajax_submission/webserver_html_simple"+target #TODO

            with open(htmlFilePath, 'rb') as fin:
                self.copyfile(fin, self.wfile)
            return
        else:
            if platform.startswith("linux"):
                htmlFilePath = os.getcwd() + "/ajax_submission/webserver_html_simple/index.html"
            elif platform.startswith("win32"):
                htmlFilePath = os.getcwd() + "/ajax_submission/webserver_html_simple/index.html" #TODO

            with open(htmlFilePath, 'rb') as fin:
                self.copyfile(fin, self.wfile)
        

        return

handler = AtousaHttpRequestHandler

PORT = 9092
my_server = socketserver.TCPServer(("", PORT), handler)

my_server.serve_forever()