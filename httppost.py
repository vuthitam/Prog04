# python3 httppost.py --url http://blogtest.vnprogramming.com/ --username test --password test123QWE@AD
# python3 httppost.py --url http://blogtest.vnprogramming.com/ --username test --password test123QWE@ADabc

import socket
import sys
from argparse import ArgumentParser

def getParameter():
    argparser = ArgumentParser()
    argparser.add_argument("--url", help='Ban nho nhap URL')
    argparser.add_argument("--username", help='Ban nho nhap username')
    argparser.add_argument("--password", help='Ban nho nhap password')
    args = argparser.parse_args()
    url = args.url
    username = args.username
    passwd = args.password
    
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
    return domain, username, passwd

#Lay toan bo du lieu cua response tra ve 
def recvAll(s):
    data = []
    response = s.recv(4096)
    while (len(response) > 0):
        data.append(response.decode())
        response = s.recv(4096)
    response = ''.join(data)
    return response

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    domain, username, password = getParameter()
    client.connect((domain, 80))
    
    # tao http post request
    body = "log="+username+"&pwd="+password+"&wp-submit=Log+In"
    request = "POST /wp-login.php HTTP/1.1\r\n"+"HOST: "+domain + "\r\n"+"Content-Length: "+str(len(body))+"\r\n"+"Content-Type: application/x-www-form-urlencoded"+"\r\n"+"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"+"\r\n"+"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"+"\r\n" + "Cookie: wordpress_test_cookie=WP Cookie check; wp_lang=en_US \r\n"+ "\r\n"+body
    # print(request)
    client.send(request.encode())
    response = recvAll(client)
    if "HTTP/1.1 302 Found" in response and "is incorrect" not in response and "is not registered on this site" not in response:
    	print("Dang nhap thanh cong.")
    else:
    	print("Dang nhap that bai.")     	

main()