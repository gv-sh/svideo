import socket
import random
import time

HOST = 'localhost'    # The remote host
PORT = 8765           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while True:
    s.connect((HOST, PORT))
    while True:
        s.send('READY')
        data = s.recv(1024)
        print('Server > ' + data)
        time.sleep(1)
s.close()
   