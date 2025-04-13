from genericpath import exists
import socket
from struct import pack
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

    RttList = []
    packetLoss = 0

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
                Rtt = (end - start) * 1000  # convert to milliseconds
                RttList.append(Rtt)

                print ("RTT: " + str(Rtt) + " ms \n")

            except socket.timeout:
                print( "#" + str(i) + " Requested timed out \n")
                packetLoss += 1
    finally:
        print("closing socket")
        mysocket.close()

    print("\n----------------------------------")
    print("Ping statistics")
    print("-----------------------------------")

    packetReceived = 10 - packetLoss

    if len(RttList) > 0:
        print("Minimum RTT: " + str(min(RttList)) + "ms")
        print("Maximum RTT: " + str(max(RttList)) + "ms")
        print("Average RTT: " + str(sum(RttList)/len(RttList)) + "ms")
    else:
        print("all packets lost, " + str(packetReceived) + " packets received")

    loss_rate = (packetLoss / 10) * 100

    print("Packets Lost: " + str(packetLoss) + "/10")
    print("Packet Loss Rate: " + str(loss_rate) + "%")

