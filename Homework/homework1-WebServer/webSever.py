# Update date: 2020/12/14
# Author: Zhuofan Zhang
import socket
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=80)
parser.add_argument('--buff', type=int, default=1024)
parser.add_argument('--filedir', type=str, default='./files')
args = parser.parse_args()

# Material path
fileDir = args.filedir

# Provide mainly HTTP response
Host = ''
servicePort = args.port

# Open the listen socket
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.bind((Host, servicePort))
listenSocket.listen(1)

# The recv-data bufsize
buffSize = args.buff

while True:
    connectSocket, addr = listenSocket.accept()
    print("connect success to {}".format(addr))
    recvData = connectSocket.recv(buffSize).decode()
    print("recv Data: {}".format(recvData))
    requestFile = recvData.split()[1]
    if requestFile[-4:] == 'html':
        with open(os.path.join(fileDir, requestFile), 'r') as rfile:
            responseData = rfile.read()
            responseHeader = "HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: {}\n\n".format(len(responseData))
            connectSocket.send(responseHeader.encode())
            connectSocket.send(responseData.encode())
    connectSocket.close()






