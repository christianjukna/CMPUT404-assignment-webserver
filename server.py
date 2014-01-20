import SocketServer
import os
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        # Split the request for parsing
        # 0 - Request
        # 1 - File Path
        requestData = self.data.split()
        baseUrl = '/www'

        # Check if the filepath leads out of the www directory
        if "../" in requestData[1]:
            error = ("HTTP/1.1 404 Not Found\n")
            self.request.sendall(error)
            return  
        
        filePath = self.append_index(os.getcwd() + baseUrl + requestData[1])
        # Make Sure is is a GET command
        if "GET" != requestData[0]: 
            error = ("HTTP/1.1 501 Not Implemented\n")
            self.request.sendall(error)
            return         

        # Handle all the possible requests and respond according to HTTP
        # error codes
        print filePath
        if os.path.isfile(filePath) and "../" not in filePath :  
            response = ("HTTP/1.1 200 OK\n" +
            "Content-Type: "+self.html_or_css(filePath)+"\n\n"
            + open(filePath,"r").read() +"\n")
            self.request.sendall(response)
            return
        else:
            error = ("HTTP/1.1 404 Not Found\n")
            self.request.sendall(error)
            return  
        
    def html_or_css(self,fileRequest):
        fileType = os.path.splitext(fileRequest)[1]
        if (fileType == ".css"):
            return "text/css"
        if fileType == ".html":
            return "text/html"
        
    def append_index(self,fileRequest):
        fileRequest = os.path.realpath(fileRequest)
        if (os.path.isdir(fileRequest)):
            return fileRequest + "/index.html"
        else:
            return fileRequest
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
