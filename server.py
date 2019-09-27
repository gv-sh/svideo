'''
.. module:: server
   :platform: Raspberry Pi
   :synopsis: Synchronous video playback across multiple raspberry pi

.. moduleauthor:: 0xf17 <grv@mathscapes.xyz>

'''

from svideo import *

s       = None
clients = []
READY   = False

def preload():
    ''' Create and bind socket
    '''
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

def is_not_connected(caddr):
    ''' Checks if client is still not connected to master
    '''
    global clients 
    for client in clients:
        if caddr == client['addr']:
            return False
    return True

def wait_for_all_connections(csocket, caddr):
    ''' Wait for confirmation from `client` for READY status
    '''
    global clients
    
    if is_not_connected(caddr):   
        msg = pickle.loads(csocket.recv(1024))
        log(caddr, 'master', msg)

        if msg['cmd'] == 'READY': 
            clients.append({'socket': csocket, 'addr': caddr})
            msg = { 'cmd'           : 'ACK', 
                    'response_to'   : 'READY'
            }
            csocket.send(pickle.dumps(msg))
            log('master', caddr, msg)

def request_playback(client, seek_to, scheduled_time):
    ''' Request `client` to start the video from `seek_to` seconds at the `scheduled_time`
    '''
    csocket = client['socket']
    msg = { 'cmd'           : 'PLAY', 
            'seek_to'       : seek_to,
            'scheduled_time': scheduled_time
    }
    csocket.send(pickle.dumps(msg))
    log('master', client['addr'], msg)

def init():
    while len(clients) < MAX_CLIENTS:
        conn, addr = s.accept()
        T = threading.Thread(target = wait_for_all_connections, args = (conn, addr))
        T.start()

def main():
    log('master', 'user', 'Initiating svideo...')
    
    try:
        init()
        log('master', 'user', 'All clients READY')
        
        scheduled_start_time = datetime.datetime.now() + datetime.timedelta(seconds=60)

        for c in clients:
            request_playback(c, 0, scheduled_start_time)

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

if __name__ == "__main__":
    preload()
    main()