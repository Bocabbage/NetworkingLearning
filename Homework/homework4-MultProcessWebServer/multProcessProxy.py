# Update date: 2020/12/16
# Author: Zhuofan Zhang
import socket
import os
import argparse
import threading

def request_parse(request):
    '''
        parse the request from the client.
    '''
    lines = request.replace('\r\n', '\n').split('\n')
    requestLine = lines[0]
    headerLines = lines[1:]
    headerTokens = {}

    for line in headerLines:
        key = line[:line.find(':')]
        value = line[line.find(':')+1 :].strip()
        headerTokens[key] = value
    
    return requestLine, headerTokens

def url_host_parser(requestURL):
    tmpHost, _, url = requestURL.partition('//')[2].partition('/')
    ifSpecialPort =  tmpHost.find(':') 
    if ifSpecialPort != -1:
        host = tmpHost[:ifSpecialPort]
        port = int(tmpHost[ifSpecialPort + 1:])
    else:
        host = tmpHost
        port = 80
    return host, port, url

def proxy(connectSocket, addr, buffSize):
    '''
        Proxy function: Connect to a client, receive its request
                        and work like a proxy.
        Note: This function is called threading-concurrently.
    '''
    print("proxy connect success to {}".format(addr))
    httpRequest = connectSocket.recv(buffSize).decode()
    requestLine, headerTokens = request_parse(httpRequest)

    method = requestLine.split(' ')[0]
    host, port, url = url_host_parser(requestLine.split(' ')[1])

    if method == 'GET':
        # # The proxy is set as web proxy defaultly
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        print("client connect success to {}".format(host))

        # Construct the HTTP request
        proxyRequest = "GET {} HTTP/1.1\n".format(url)
        for key, value in headerTokens.items():
            proxyRequest  = proxyRequest + key + ":" + value + "\n"
        
        clientSocket.send(proxyRequest.encode())
        response = clientSocket.recv(buffSize)
        clientSocket.close()

        print("proxy GET http:")
        print(response.decode())

        connectSocket.send(response)
        connectSocket.close()

    connectSocket.close()
    
   
    



parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=10086)
parser.add_argument('--buff', type=int, default=10240)
parser.add_argument('--thread', type=int, default=10)
args = parser.parse_args()

# Maximum thread number
maxThreads = args.thread

# Provide mainly HTTP response
Host = ''
servicePort = args.port

# Open the listen socket
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.bind((Host, servicePort))
listenSocket.listen(1000)

# The recv-data bufsize
buffSize = args.buff

while True:
    connectSocket, addr = listenSocket.accept()
    th = threading.Thread(target=proxy, args=(connectSocket, addr, buffSize))
    th.start()
