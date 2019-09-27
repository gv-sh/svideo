import socket
import threading
import time
import pickle 
import sys
import datetime 

HOST        = 'rpi1'
PORT        = 8765
MAX_CLIENTS = 2

def log(fr, to, msg):
    ''' print log of happened communication
    '''

    print(str(fr) + ' > ' + str(to) + ' : ' + str(msg))