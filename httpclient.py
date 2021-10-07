#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return int(data.split()[1])

    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        if(len(data.split("\r\n\r\n"))>=2):
            return data.split("\r\n\r\n")[1]
        else:
            return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""


        urlResult = urllib.parse.urlparse(url)
        path = urlResult.path
        host = urlResult.hostname
        port = 80
        if(urlResult.port):
            port = urlResult.port



        request = ""

        #clarify the request method and http version
        if(path == ""):
            request += "GET / HTTP/1.1\r\n"
        else:
            request += "GET "+path+" HTTP/1.1\r\n"


        #hostname
        request += "Host: "+host+":"+str(port)+"\r\n"

        #accept MIME
        request += "Accept: */*;q=0.8\r\n"

        #accept language
        request += "Accept-Language: en-US,en;q=0.5\r\n"

        #encoding
        request += "Accept-Encoding: *\r\n"

        #connection status
        # request += "Connection: keep-alive\r\n\r\n"
        request += "Connection: close\r\n\r\n"
        self.connect(host,port)
        self.sendall(request)
        responseData = self.recvall(self.socket)
        #print(responseData)
        self.close()

        # print(self.get_code(responseData))
        # print(self.get_headers(responseData))
        # print()
        # print(self.get_body(responseData))
        code = self.get_code(responseData)
        body = self.get_body(responseData)

        #print(f"GET RESULT:\n{self.get_headers(responseData)}\n{self.get_body(responseData)}")
        print(f"GET RESULT:\n"+responseData)

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        request = ""

        urlResult = urllib.parse.urlparse(url)
        path = urlResult.path
        host = urlResult.hostname
        port = 80
        if(urlResult.port):
            port = urlResult.port

        #query the request body
        requestBody = ""
        if(args):
            requestBody = urllib.parse.urlencode(args)

        request = ""

        #clarify the request method and http version
        if(path == ""):
            request += "POST / HTTP/1.1\r\n"
        else:
            request += "POST "+path+" HTTP/1.1\r\n"

        #hostname
        request += "Host: "+host+":"+str(port)+"\r\n"

        #Content-Type
        request += "Content-Type: application/x-www-form-urlencoded\r\n"

        #Content-Length
        request += "Content-Length: " + str(len(requestBody)) + "\r\n"

        #accept MIME
        request += "Accept: */*;q=0.8\r\n"

        #accept language
        request += "Accept-Language: en-US,en;q=0.5\r\n"

        #encoding
        request += "Accept-Encoding: *\r\n"

        #connection status
        # request += "Connection: keep-alive\r\n\r\n"
        request += "Connection: close\r\n\r\n"

        #request body
        request += requestBody


        self.connect(host,port)
        self.sendall(request)
        responseData = self.recvall(self.socket)
        #print(responseData)
        self.close()

        # print(self.get_code(responseData))
        # print(self.get_headers(responseData))
        # print()
        # print(self.get_body(responseData))


        code = self.get_code(responseData)
        body = self.get_body(responseData)

        #print(f"POST RESULT:\n{self.get_headers(responseData)}\r\n\r\n{self.get_body(responseData)}")
        print(f"POST RESULT:\n"+responseData)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
