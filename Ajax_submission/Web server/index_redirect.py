import http.server
import socketserver
import os 

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        filename = self.path

        if filename == '/index.html' or filename == "/":
            file_path = os.getcwd() + '/index.html'
        else:
            file_path = os.path.dirname(os.getcwd()) + '/API/files' + filename
            

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fin:
                self.copyfile(fin, self.wfile)

        return

handler_object = AtousaHttpRequestHandler 
PORT = 8080
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()