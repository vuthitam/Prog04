# python3 httpdownload.py --url http://blogtest.vnprogramming.com/ --remotefile http://blogtest.vnprogramming.com/wp-content/uploads/2022/03/image-3.jpg
# python3 httpdownload.py --url http://blogtest.vnprogramming.com/ --remotefile http://blogtest.vnprogramming.com/wp-content/uploads/2022/03/image-abc.jpg
import socket
import sys
from argparse import ArgumentParser

def getParameter():
    argparser = ArgumentParser()
    argparser.add_argument("--url", help='Ban nho nhap URL')
    argparser.add_argument("--remotefile", help='Ban nho nhap path file to download')
    args = argparser.parse_args()
    url = args.url
    pathFile = args.remotefile  
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
    return domain, pathFile

def receiveData(socket):
    data = []
    response = socket.recv(4096)
    while (len(response) > 0):
        data.append(response)
        response = socket.recv(4096)
    response = b''.join(data)
    return response

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    domain, pathFile = getParameter()
    client.connect((domain, 80))
    request = "GET "+pathFile+" HTTP/1.1\r\n"+"Host: "+domain+"\r\n"+"\r\n"
    client.send(request.encode())
    response = receiveData(client)
    
    len_image = b""
    if b"HTTP/1.1 200 OK" in response:
        for i in range(0, len(response)):
            if len_image != b"":
                break
            if response[i:i+16] == b"Content-Length: ":
            
                for j in range(i+16, len(response)):
                    if(not chr(response[j]).isdigit()):
                        len_image = response[i+16:j]
                        break
    else:
        print("Khong ton tai file anh.")
        return
    print("Kich thuoc file: "+len_image.decode()+" bytes")
    content_file = response.split(b"\r\n\r\n")[1]
    
    fileName = pathFile.split('/')[-1]
    location = "/tmp/"+fileName
    open(location, "wb").write(content_file)
main()