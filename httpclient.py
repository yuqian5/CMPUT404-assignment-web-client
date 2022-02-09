#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, Kerry Cao
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

import socket
import sys


# you may use urllib to encode data appropriately
from urllib.parse import urlparse

from httputility import *


def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    # def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self, data):
        return None

    def get_body(self, data):
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
        sock.close()
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # parse url
        request = urlparse(url)

        # establish a socket connection
        self.connect(request.hostname, request.port if request.port is not None else 80)

        # get query
        body = args_2_url_encode(args)
        query = f"{request.query}{'&' if request.query != '' and body != '' else ''}{body}"

        # forming request header
        get_request = f"GET {request.path if request.path != '' else '/'}{'?' if query != ''  else ''}{query} HTTP/1.1\r\nHost: {request.hostname}\r\nUser-Agent: SAWC/1.1\r\nConnection: close\r\n\r\n"

        # send request
        self.sendall(get_request)

        # get response
        resp = self.recvall(self.socket)

        resp_parsed = parse_response(resp)

        return HTTPResponse(resp_parsed["code"], resp_parsed["body"])

    def POST(self, url, args=None):
        # parse url
        request = urlparse(url)

        # establish a socket connection
        self.connect(request.hostname, request.port if request.port is not None else 80)

        # get body
        body = args_2_url_encode(args)

        # forming request header
        post_request = f"POST {request.path if request.path != '' else '/'}{'?' if request.query != '' else ''}{request.query} HTTP/1.1\r\nHost: {request.hostname}\r\nUser-Agent: SAWC/1.1\r\nConnection: close\r\n"
        post_request += f"Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(body)}\r\n\r\n"
        post_request += body

        # send request
        self.sendall(post_request)

        # get response
        resp = self.recvall(self.socket)

        resp_parsed = parse_response(resp)

        return HTTPResponse(resp_parsed["code"], resp_parsed["body"])

    def command(self, url, command="GET", args=None):
        if command == "POST":
            return self.POST(url, args)
        else:
            return self.GET(url, args)


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if len(sys.argv) <= 1:
        help()
        sys.exit(1)
    elif len(sys.argv) == 3:
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
