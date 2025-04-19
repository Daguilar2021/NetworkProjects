#SMTPClient.py
# Mail client

from socket import *
import base64

# Mailtrap SMTP server details
mailserver = ("sandbox.smtp.mailtrap.io", 2525)  # Port 25, 465, 587, or 2525

# Mailtrap credentials (use actual username/password)
username = "7b0aac883cbab8"
password = "86f296c6945fb5"  # Replace with actual password

msg = "\r\n I love computer networks! \n[This is a test email sent from my raw Python SMTP client for Project 3!]"
endmsg = "\r\n.\r\n"

# Create TCP socket (called clientSocket) and connect to Mailtrap server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# Receive server greeting
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send EHLO command (HELO like EHLO)
ehloCommand = 'EHLO studentClient\r\n'
clientSocket.send(ehloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)

# AUTH LOGIN with base64-encoded username and password
clientSocket.send('AUTH LOGIN\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)

clientSocket.send(base64.b64encode(username.encode()) + b'\r\n')
recv3 = clientSocket.recv(1024).decode()
print(recv3)

clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv4 = clientSocket.recv(1024).decode()
print(recv4)

# Send MAIL FROM command and print server response
clientSocket.send('MAIL FROM:<test@mailtrap.io>\r\n'.encode())
recv5 = clientSocket.recv(1024).decode()
print(recv5)

# Send RCPT TO (you can view this in Mailtrap inbox)
clientSocket.send('RCPT TO:<to@example.com>\r\n'.encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)

# Send DATA command and print server response
clientSocket.send('DATA\r\n'.encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)

# Send message data/ body
clientSocket.send(msg.encode())

# End the message with period on its own line
clientSocket.send(endmsg.encode())
recv8 = clientSocket.recv(1024).decode()
print(recv8)

# Send QUIT command and get server response
clientSocket.send('QUIT\r\n'.encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)

# Close the socket
clientSocket.close()
