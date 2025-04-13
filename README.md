# NetworkProjects

This repository contains a collection of small but foundational network programming assignments built in Python. 
---

## Project Contents

### 🌐 1. Web Server
A simple Python based HTTP server that:
- accepts single browser request
- parse the request to determine the specific file being requested
- get the requested file from the server’s file system
- create an HTTP response message consisting of the requested file preceded by header lines
- sends the response over the TCP connection to the requesting browser.

### 2. UDP Client Pinger
A Python Client side application that sends 10 UDP ping messages to the server.
it does the following:
- Application waits up to 1 second for response
- returns message Round Trip Time (RTT)
- Handles packet loss

### 3. Mail client
Basic python Mail client
