import socket
import threading
import time
import pickle 
import sys
import datetime 
import os

HOSTS               = ['192.168.0.100', '192.168.0.105', '192.168.0.106']
HOST                = HOSTS[0]
PORT                = 8766
MAX_CLIENTS         = 2
LISTENING_TIME_OUT  = 1.0

def log(fr, to, msg):
    ''' print log of happened communication '''
    print(str(fr) + ' > ' + str(to) + ' : ' + str(msg))