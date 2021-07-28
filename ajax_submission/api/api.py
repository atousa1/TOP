import http.server
import socketserver
import re
import os 
import json
import cgitb
import cgi
import cgitb
from sys import platform
import mysql.connector

cgitb.enable()


class User:

    def __init__(self, inp_id, inp_name, inp_age, inp_city):
        self.id = inp_id
        self.name = inp_name
        self.age = inp_age
        self.city = inp_city

def UserParser(data_str):

    user_dict = json.loads(data_str)
    nat_id = user_dict["National_ID"]
    name = user_dict["Name"]
    age = user_dict["Age"]
    city = user_dict["City"]
    new_user = User(nat_id, name, age, city)
    return new_user

def ConnectSqlServer():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="top")
    curs = conn.cursor()
    return conn, curs

def TableDrawer(conn, curs):
    
    conn, curs = ConnectSqlServer()

    sql = "SELECT * FROM usersregisteration"
    curs.execute(sql)
    # conn.commit()

    html = "<style> table, th, td { border: 1px solid black; }</style> <table>   <tr> <th>ID</th> <th>National ID</th> <th>Name</th> <th>Age</th> <th>City</th> </tr>"
    row = curs.fetchone()
    if row is not None:
        while row is not None:
            print(row)
            table_row = "<tr><td>" + str(row[0]) + "</td><td>" + str(row[1]) + "</td><td>"+ str(row[2]) + "</td><td>"+ str(row[3]) + "</td><td>"+ str(row[4]) + "</td></tr>"
            html += table_row
            row = curs.fetchone()
        html += "</table>"

    elif row is None:
        html = "This National ID is registered before."

    curs.close()
    conn.close()
    return html

class AtousaHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")

        self.end_headers()

        target = self.path
        pattern = r'^/user/\d+$'
        


        if target == '/users':
            if platform.startswith("linux"):
                filepath = os.getcwd() + "/ajax_submission/api/files/data.json"
            elif platform.startswith("win32"):
                filepath = os.getcwd() + "/files/data.json"
            with open(filepath, 'rb') as json_str:                
                self.copyfile(json_str, self.wfile)
            return

        elif target == '/user':

            # if platform.startswith("linux"):
            #     htmlFilePath = os.getcwd() + "/ajax_submission/webserver_html_simple/user.html"
            # elif platform.startswith("win32"):
            htmlFilePath = os.getcwd() + "/ajax_submission/webserver_html_simple/user.html" #TODO

            with open(htmlFilePath, 'rb') as fin:
                self.copyfile(fin, self.wfile)
            return

        elif target == '/usersd':

            conn, curs = ConnectSqlServer()
            html = TableDrawer(conn, curs)
            self.wfile.write(bytes(html, "utf8"))
            
            return 
            
        elif re.match(pattern, target):
            if platform.startswith("linux"):
                filepath = os.getcwd() + "/ajax_submission/api/files/data.json"
            elif platform.startswith("win32"):
                filepath = os.getcwd() + "/files/data.json"
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

            html = "Atousa does not know what to do with your GET request :)"
            self.wfile.write(bytes(html, "utf8"))
            return
  

    def do_POST(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")

        data_byte = self.rfile.read(int(self.headers['Content-Length']))

        self.end_headers()        
        
        target = self.path

        if target == '/user':

            ## without using classes
            '''
            # new_user = {}
            # new_user_data = {}
            # for key in data_dict.keys():
            #     if key in ['Name', 'Age', 'City']:
            #         new_user_data[key] = data_dict[key]
            # new_user[str(data_dict['ID'])] = new_user_data
            '''

            ## using classes
            data_str = data_byte.decode("utf-8")
            new_user = UserParser(data_str)
            conn, curs = ConnectSqlServer()

            sql = "SELECT * FROM usersregisteration WHERE National_ID='"+str(new_user.id)+"'"
            curs.execute(sql)
            # conn.commit()
            msg = curs.fetchall()

            if len(msg)!=0:
                add_user_flag = False
                html = "This National ID is registered before."
            else:
                add_user_flag = True

            if add_user_flag:
                sql_query = "INSERT INTO usersregisteration(National_ID, Name, Age, City) VALUES(%s, %s, %s, %s);"
                curs.execute(sql_query, (new_user.id, new_user.name, new_user.age, new_user.city))
                conn.commit()
                curs.close()
                conn.close()

                # if platform.startswith("linux"):
                #     jsonFilePath = os.getcwd() + "/ajax_submission/api/files/data.json"
                # elif platform.startswith("win32"):
                #     jsonFilePath = os.getcwd() + "/files/data.json"

                # with open(jsonFilePath, 'r+') as jsonSrc_str:

                #     jsonSrc = json.load(jsonSrc_str)
                #     jsonSrc.update(new_user)
                #     jsonSrc_str.seek(0)
                #     json.dump(jsonSrc, jsonSrc_str, indent=4)

                html = "User {} is added to database.".format(new_user.name)

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