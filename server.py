from svideo import *

s       = None
clients = []
READY   = False

def preload():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

def is_not_connected(caddr):
    global clients 
    for client in clients:
        if caddr == client['addr']:
            return False
    return True

def wait_for_all_connections(csocket, caddr):
    global clients, READY
    
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
    csocket = client['socket']
    msg = { 'cmd'           : 'PLAY', 
            'seek_to'       : seek_to,
            'scheduled_time': scheduled_time
    }
    csocket.send(pickle.dumps(msg))
    log('master', client['addr'], msg)

def main():
    log('master', 'user', 'Initiating svideo...')
    
    try:
        while len(clients) < MAX_CLIENTS:
            conn, addr = s.accept()
            T = threading.Thread(target = wait_for_all_connections, args = (conn, addr))
            T.start()
        
        log('master', 'user', 'All clients READY')

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

if __name__ == "__main__":
    preload()
    main()