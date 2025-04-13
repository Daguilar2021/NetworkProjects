import socket
import time

while True:
    print("\nThis is the UDP Client to Ping to the UDP server press the following")
    print("-----------------------------------")
    print("a. press any key to ping to the server")
    print("b. press q to exit out the program")
    print("----------------------------------- \n")

    choice = input("enter your choice: ")
    if choice.lower() == 'q':
        break

    print("\n-----------------------------------")
    print("start pinging server")
    print("----------------------------------- \n")

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 12000)
    mysocket.settimeout(1)

    try:
        for i in range(0,10):
            start = time.time()
            message = 'ping #' + str(i) + " " + time.ctime(start)
            try:
                mysocket.sendto(message.encode(), server_address)
                print ("sent " + message)
                data, server = mysocket.recvfrom(4096)
                
                print("received " + str(data))

                end = time.time()
                Rtt = end - start
                print ("RTT: " + str(Rtt * 1000) + " ms \n")

            except socket.timeout:
                print( "#" + str(i) + " Requested timed out \n")
    finally:
        print("closing socket")
        mysocket.close()