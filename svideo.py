import socket
import threading
import time
import pickle 
import sys

HOST        = 'localhost'
PORT        = 8765
MAX_CLIENTS = 2

def log(fr, to, msg):
    print(str(fr) + ' > ' + str(to) + ' : ' + str(msg))
