#! /usr/bin/env python3
from datetime import datetime 

from socket import AF_INET, SOCK_STREAM, socket

server_port = 15000
server_socket = socket(AF_INET, SOCK_STREAM)
try:
    server_socket.bind(("", server_port))
except: server_port = int(input("Port already in use, give a different port:"))

def read_file(file_path):

    with open("." +file_path,"r") as f:
        file_content = f.read()
        return file_content.encode()

def return_404(client_version):
        response_header = (
        f"{client_version} 404 Not Found \r\n"
        "Connection: close\r\n"
        "\r\n")
        return response_header

def return_405(client_version):
        response_header = (
        f"{client_version} 405 Method Not Allowed \r\n"
        "Connection: close\r\n"
        "\r\n")
        return response_header

def return_400():
        response_header = (
            "HTTP/1.1 400 Bad Request \r\n"
            "Connection: close\r\n"
            "\r\n")
        return response_header

def return_200(file_to_send, client_version):
        response_header = (
        f"{client_version} 200 OK \r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(file_to_send)}\r\n"
        "Connection: close\r\n"
        "\r\n")
        return response_header
    
def log(date_time, ip, hhtp_call, status_code, size_of_response_file):
    log_message = f'{ip} - - [{date_time}] - - "{hhtp_call}" {status_code} {size_of_response_file}\n'
    with open("log.txt","a") as f:
        f.write(log_message)
    

server_socket.listen(1)
print("The server is ready to recieve.")
while True:
    connection_socket, addr = server_socket.accept()
    msg = connection_socket.recv(2048)
    print(f"This address has connected {addr}")

    msg_decode = msg.decode()
    first_line = msg_decode.split("\r\n")[0]
    date_and_time = datetime.now()

    if len(first_line.split()) != 3:
        header = return_400().encode()
        log(date_and_time, addr[0], first_line, 400, 0)
        connection_socket.send(header)
        connection_socket.close()
    else:
        method = first_line.split()[0]
        path = first_line.split()[1]
        client_version = first_line.split()[2]
        if not client_version.startswith("HTTP/"):
            header = return_400().encode()
            log(date_and_time, addr[0], first_line, 400, 0)
            connection_socket.send(header)
            connection_socket.close()
        elif method != "GET":
            header = return_405(client_version).encode()
            log(date_and_time, addr[0], first_line, 405, 0)
            connection_socket.send(header)
            connection_socket.close()        
        else:        
            if path == "/" or path == "/index.html":
                file_to_send = read_file("/index.html")
                header = return_200(file_to_send, client_version).encode()
                log(date_and_time, addr[0], first_line, 200, len(file_to_send))
                connection_socket.send(header)
                connection_socket.send(file_to_send)

            elif path == "/test.html":
                file_to_send = read_file(path)
                header = return_200(file_to_send, client_version).encode()
                log(date_and_time, addr[0], first_line, 200, len(file_to_send))
                connection_socket.send(header)
                connection_socket.send(file_to_send)
            else:
                header = return_404(client_version).encode()
                log(date_and_time, addr[0], first_line, 404, 0)
                connection_socket.send(header)
        
        connection_socket.close()

