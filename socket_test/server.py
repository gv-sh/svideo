'''
               +-----------------+              
               |                 |              
+--------------v--------------+  |              
|  Wait for all connections   |  |              
+--------------+--------------+  |              
               |                 |              
       +-------v------+          |              
    +--|  All READY?  +----No----+              
    |  +--------------+                         
    |                                           
    +--Yes-----+                                
               |                                
               v                                
+--------------------+   +---------------------+
| Send START to all  +--->   Start playback    |
+--------------+-----+   +---------------------+
               |                                
+--------------v-----+   +---------------------+
|  Poll every 3 min  +---> Send SYNC commands  |
+--------------------+   +---------------------+                           
'''

import socket
import threading
import time

HOST = 'localhost'        # Symbolic name meaning all available interfaces
PORT = 8765               # Arbitrary non-privileged port
MAX_CLIENTS = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

clients = []
READY = False

def isNotConnected(caddr):
    global clients 
    for client in clients:
        if caddr == client['addr']:
            return False
    return True

def waitForAllConnections(csocket, caddr):
    global clients
    if isNotConnected(caddr):   
        data = csocket.recv(1024)
        if data == 'READY':
            print(str(caddr) + '> READY')
            clients.append({'socket': csocket, 'addr': caddr})
            csocket.send('ACK')
    if len(clients) == MAX_CLIENTS:
        READY = True
        print('All clients READY')

def requestPlayback(client):
    global clients 
    
def handleClient(csocket, caddr):
    while True:
        data = csocket.recv(1024)
        print(str(caddr) + ': ' + data)
        csocket.send('OK')
    csocket.close()

while True:
    if not READY:
        conn, addr = s.accept()
        T = threading.Thread(target = waitForAllConnections, args = (conn, addr))
        T.start()

s.close()