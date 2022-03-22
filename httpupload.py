# python3 httpupload.py --url http://blogtest.vnprogramming.com/ --username test --password test123QWE@AD --localfile /home/tamvt/Desktop/image.jpg
# python3 httpupload.py --url http://blogtest.vnprogramming.com/ --username tamvt --password tamtit --localfile /home/tamvt/Desktop/image.jpg

import socket
import sys
import string
import re
from argparse import ArgumentParser

def getParameter():
    argparser = ArgumentParser()
    argparser.add_argument("--url", help='Ban nho nhap URL')
    argparser.add_argument("--username", help='Ban nho nhap username')
    argparser.add_argument("--password", help='Ban nho nhap password')
    argparser.add_argument("--localfile", help='Ban nho nhap path file image')
    args = argparser.parse_args()
    url = args.url
    username = args.username
    passwd = args.password
    pathLocalFile = args.localfile
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
    return domain, username, passwd, pathLocalFile



def receiveData(socket):
    data = []
    response = socket.recv(4096)
    while (len(response) > 0):
        data.append(response.decode())
        response = socket.recv(4096)
    response = ''.join(data)
    return response

def getCookies(response):
    cookies = []
    line = response.split("\r\n")
    for i in line:
        if "Set-Cookie: " in i:
            cookies.append(i.split(";")[0].split(":")[1].strip())
    return ";".join(cookies)
    

def getWpNonce(cookies, domain):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((domain, 80))
    valid = string.ascii_lowercase+string.digits
    
    request = "GET /wp-admin/media-new.php HTTP/1.1\r\n" + \
        "Host: "+domain+"\r\n"+"Cookie: "+cookies+"\r\n\r\n"
    
    client.send(request.encode())
    response = receiveData(client)
    start = re.search('name="_wpnonce"', response).end() + 8
    end = start + 10
    return response[start:end]
    return result


def uploadImage(cookies, domain, filename, localfile):
    file_img = open(localfile, 'rb').read()
    wpnonce = getWpNonce(cookies, domain)
    file_type = filename.split(".")[-1]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((domain, 80))
    
    req_body = "------WebKitFormBoundary"+"\r\n" + \
	"Content-Disposition: form-data; name=\"name\"" + "\r\n\r\n"+filename+"\r\n"+"------WebKitFormBoundary"+"\r\n" + \
	"Content-Disposition: form-data; name=\"action\"" + "\r\n\r\n" + "upload-attachment"+"\r\n" + "------WebKitFormBoundary" + "\r\n" + \
	"Content-Disposition: form-data; name=\"_wpnonce\""+"\r\n\r\n"+wpnonce+"\r\n"+"------WebKitFormBoundary" + "\r\n" + \
	"Content-Disposition: form-data; name=\"async-upload\"; filename=\"" + filename + "\""+"\r\n" + \
	"Content-Type: image/"+file_type+"\r\n\r\n"
    req_body = req_body.encode() + file_img + b"\r\n" + b"------WebKitFormBoundary--\r\n"
    
    request = "POST /wp-admin/async-upload.php HTTP/1.1\r\n"+"Host: " + domain + "\r\n" 
    request += 'Cookie:' + cookies + '\r\n'
    request += "Connection: keep-alive\r\n"
    request += "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\n"    
    request += "Content-Length: " + str(len(req_body)) + "\r\n\r\n"
    request = request.encode() + req_body   

    client.send(request)
    response = receiveData(client)
    
    if "HTTP/1.1 200 OK" in response and "{\"success\":true" in response:
        print("Upload success.")
        path_image = ""
        for i in range(0, len(response)):
            if(path_image != ""):
                break
            if response[i:i+7] == "\"url\":\"":
                for j in range(i+7, len(response)):
                    if(response[j] == "\""):
                        break
                    path_image += response[j]
        path_image = path_image.replace('\\', '')
        print("File upload url:"+path_image)
    else:
        print("Upload fail.")
    return
    
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    domain, username, password, pathLocalFile = getParameter()
    
    fileName = pathLocalFile.split("/")[-1]
    client.connect((domain, 80))
    req_body = "log="+username+"&pwd="+password+"&wp-submit=Log+In"
    request = "POST /wp-login.php HTTP/1.1\r\n"+"HOST: "+domain + "\r\n"+"Content-Length: "+str(len(req_body))+"\r\n"+"Content-Type: application/x-www-form-urlencoded"+"\r\n"+"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"+"\r\n"+"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"+"\r\n" + "Cookie: wordpress_test_cookie=WP Cookie check; wp_lang=en_US"+"\r\n" \
    "\r\n"+req_body
    
    client.send(request.encode())
    response = receiveData(client)
    
    if "HTTP/1.1 302 Found" in response and "is incorrect" not in response and "is not registered on this site" not in response:
        cookies = getCookies(response)
        uploadImage(cookies, domain, fileName, pathLocalFile)
    else:
        print("User "+username+" dang nhap that bai.")

main()