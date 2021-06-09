import http.server
import socketserver
import re
import os 
import json
import cgitb
import cgi
import cgitb
cgitb.enable()


class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()

        target = self.path
        pattern = r'^/user/\d+$'
        
        filepath = os.getcwd() + "/ajax_submission/api/files/data.json"

        if target == '/users':
            
            with open(filepath, 'rb') as json_str:                
                self.copyfile(json_str, self.wfile)
            return

        elif re.match(pattern, target):

            user_id = target.split("/")[-1]
            with open(filepath, 'r') as json_str: 

                data_obj = json.load(json_str)

                if user_id in data_obj:
                    user = data_obj[user_id]
                    json_user = json.dumps(user)
                else:
                    json_user = "Oops! I can't find this user!"

                self.wfile.write(bytes(json_user, "utf8"))
            return
        else:

            html = "Atousa does not know what to do with your GET request :) and target:{}" .format(form)
            self.wfile.write(bytes(html, "utf8"))
            return
  

    def do_POST(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")

        a = self.rfile.read(int(self.headers['Content-Length']))
        print(a.__str__())

        self.end_headers()

        target = self.path

        if target == '/user':

            html = f"<html><head></head><body><h1>Create User</h1></body></html>"

        else:

            html = f"<html><head></head><body><h1>Atousa does not know what to do with your POST request :) </h1></body></html>"

        self.wfile.write(bytes(html, "utf8"))

        return

def file_presenter(filename):
    pass

handler_object = AtousaHttpRequestHandler

PORT = 7072
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()