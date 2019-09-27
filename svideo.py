'''
.. module:: svideo
   :platform: Raspberry Pi
   :synopsis: Synchronous video playback across multiple raspberry pi

.. moduleauthor:: 0xf17 <grv@mathscapes.xyz>

'''

import socket
import threading
import time
import pickle 
import sys
import datetime 

HOST        = 'localhost'
PORT        = 8765
MAX_CLIENTS = 2

def log(fr, to, msg):
    ''' print log of happened communication
    '''

    print(str(fr) + ' > ' + str(to) + ' : ' + str(msg))
