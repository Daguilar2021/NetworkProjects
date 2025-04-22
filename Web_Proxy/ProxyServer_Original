#ProxyServer.py

from socket import *
import sys
import os

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\n[server_ip: IP Address Of Proxy Server]')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8888))  # Listening on port 8888
tcpSerSock.listen(1)

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = tcpCliSock.recv(1024).decode()
    print(message)

    if not message:
        tcpCliSock.close()
        continue

    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print("Filename:", filename)

    fileExist = "false"
    filetouse = "/" + filename
    print("File to use:", filetouse)

    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.readlines()
        fileExist = "true"

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())

        for line in outputdata:
            tcpCliSock.send(line)

        print('Read from cache')

    except IOError:
        if fileExist == "false":
            # Create a socket on the proxy server
            c = socket(AF_INET, SOCK_STREAM)

            hostn = filename.replace("www.", "", 1)
            print("Host name:", hostn)

            try:
                # Connect to port 80 of the host
                c.connect((hostn, 80))

                # Send a GET request to the web server
                fileobj = c.makefile('rwb', 0)
                request_line = f"GET http://{filename} HTTP/1.0\r\n\r\n"
                fileobj.write(request_line.encode())

                # Read response into buffer
                buff = b""
                while True:
                    data = c.recv(1024)
                    if len(data) > 0:
                        buff += data
                    else:
                        break

                # Create cache file and write data
                cache_path = "./" + filename
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                tmpFile = open(cache_path, "wb")
                tmpFile.write(buff)
                tmpFile.close()

                # Send the response to the client
                tcpCliSock.send(buff)

            except Exception as e:
                print("Illegal request:", e)

        else:
            # HTTP response for file not found
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    tcpCliSock.close()

# Close the server socket when done
tcpSerSock.close()
