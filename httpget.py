# python3 httpget.py --url http://blogtest.vnprogramming.com/

import socket
import sys
import html
from argparse import ArgumentParser

def getDomain():
    argparser = ArgumentParser()
    argparser.add_argument("--url", default=None, help='Ban nho nhap URL')
    args = argparser.parse_args()
    url = args.url
    print("url:",url)
    domain = ""
    if url[0:8] == "https://":
        for i in range(8, len(url)):
            if url[i] == '/':
                break
            domain += url[i]
    if url[0:7] == "http://":
        for i in range(7, len(url)):
            if url[i] == '/':
                break
            domain += url[i]
    return domain

def recvAll(s):
    data = []
    response = s.recv(4096)
    while (len(response) > 0):
        data.append(response.decode())
        response = s.recv(4096)
    #print(data)
    response = ''.join(data)
    return response

def main():
    #domain = "blogtest.vnprogramming.com"
    domain = getDomain()
    title = ""

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((domain, 80))
    request = "GET / HTTP/1.1\r\nHOST: "+domain+"\r\n\r\n"
    request = request.encode()
    client.send(request)
    response = recv_all(client)
    for i in range(0, len(response)):
    	if title != "":
    	    break
    	if response[i:i+7] == "<title>":
    	    for j in range(i+7, len(response)):
    	        if response[j:j+8] == "</title>":
    	             title = response[i+7:j]
    	             break
    print("title:", html.unescape(title))
main()
