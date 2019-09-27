import socket
import threading
import time
import pickle 
import sys
import datetime 
import os

HOST        = '192.168.0.100'
PORT        = 8766
MAX_CLIENTS = 2

def log(fr, to, msg):
    ''' print log of happened communication
    '''

    print(str(fr) + ' > ' + str(to) + ' : ' + str(msg))