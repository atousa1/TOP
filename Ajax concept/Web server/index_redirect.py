import http.server
import socketserver
import os 

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        # self.send_header('location', 'index.html')  
        self.end_headers()

        filename = self.path
        main_folder = 'H:/For fun/TOP/Ajax concept/API/files'
        # print("inja")
        if filename == '/index.html' or filename == "":
            file_path = 'index.html'
        else:
            file_path = os.path.join(main_folder, filename)
            

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as fin:
                self.copyfile(fin, self.wfile)

        # if target == '/index.html':

        #     html = f"<html><head></head><body><h1>Create User</h1></body></html>"

        # with open('index.html', 'rb') as fin:
        #     self.copyfile(fin, self.wfile)

        return

handler_object = AtousaHttpRequestHandler 

PORT = 8080
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()