#ProxyServer.py

from urllib.parse import urlparse
from socket import *
import sys
import os
import threading

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\n[server_ip: IP Address Of Proxy Server]')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8888))  # Listening on port 8888
tcpSerSock.listen(5)

def handle_client(tcpCliSock, addr):
    print(f"[{threading.current_thread().name}] Handling connection from {addr}")
    try:
        message = tcpCliSock.recv(1024).decode()
        print(message)

        if not message:
            tcpCliSock.close()
            return

        print(message.split()[1])
        
        url = message.split()[1]
        parsed_url = urlparse(url)
        hostn = parsed_url.hostname

        if not hostn:
            print("Invalid or unsupported request. Closing connection.")
            tcpCliSock.close()
            return

        resource = parsed_url.path or "/"
        filename = hostn + resource.replace("/", "_")
        filetouse = "/" + filename
        print("Filename:", filename)

        fileExist = "false"
        print("File to use:", filetouse)

        try:
            # Check whether the file exists in the cache
            with open(filetouse[1:], "rb") as f:
                outputdata = f.read()
                fileExist = "true"

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            tcpCliSock.sendall(outputdata)

            print('Read from cache')

        except IOError:
            if fileExist == "false":
                c = socket(AF_INET, SOCK_STREAM)
                print("Host name:", hostn)

                try:
                    c.connect((hostn, 80))

                    fileobj = c.makefile('rwb', 0)
                    request_line = f"GET {resource} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                    fileobj.write(request_line.encode())

                    response = b""
                    while True:
                        data = c.recv(1024)
                        if not data:
                            break
                        response += data

                    try:
                        header_end = response.find(b"\r\n")
                        status_line = response[:header_end].decode()
                        status_code = int(status_line.split()[1])
                    except Exception as e:
                        print("Error parsing status line:", e)
                        status_code = 0 

                    tcpCliSock.send(response)

                    if status_code == 200:
                        cache_path = "./" + filename
                        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                        with open(cache_path, "wb") as tmpFile:
                            tmpFile.write(response)
                    else:
                        print(f"Response status code: {status_code}. Not caching.")

                except Exception as e:
                    print("Illegal request:", e)

            else:
                tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
                tcpCliSock.send("Content-Type:text/html\r\n".encode())
                tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    finally:
        tcpCliSock.close()

# Main server loop that spawns threads
while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    client_thread = threading.Thread(target=handle_client, args=(tcpCliSock, addr))
    client_thread.start()
