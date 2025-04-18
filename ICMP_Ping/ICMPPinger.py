#ICMPPinger.py

from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8


def checksum(source_string):
    csum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(source_string):
        csum = csum + source_string[len(source_string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)

        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fetch the ICMP header from the IP packet (first 20 bytes are IP header)
        icmpHeader = recPacket[20:28]
        type, code, checksum_recv, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

        if packetID == ID:
            # Get the data part (payload)
            timeSent = struct.unpack("d", recPacket[28:28 + struct.calcsize("d")])[0]
            rtt = (timeReceived - timeSent) * 1000
            return f"Reply from {destAddr}: bytes={len(recPacket)} time={rtt:.2f}ms"

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    myChecksum = 0

    # Create header with dummy checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)

    # Convert checksum to network byte order
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    # Create final packet with real checksum
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    try:
        mySocket = socket(AF_INET, SOCK_RAW, icmp)
    except PermissionError:
        return "You need to run this script with administrator privileges."

    myID = os.getpid() & 0xFFFF
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1, count=4):
    dest = gethostbyname(host)
    print(f"\nPinging {host} [{dest}] using Python:")
    print("")

    for i in range(count):
        result = doOnePing(dest, timeout)
        print(result)
        time.sleep(1)  # 1-second delay


if __name__ == "__main__":
    targets = [
        "127.0.0.1",            # Localhost
        "8.8.8.8",              # North America (Google)
        "baidu.com",            # Asia (China)
        "unimelb.edu.au",       # Australia
        "www.cam.ac.uk"         # Europe (UK)
    ]

    for host in targets:
        ping(host, timeout=1, count=4)
