from svideo import *

s = None 

def preload():
    ''' Setup socket to communicate with master
    '''
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def init():
    ''' Send READY status to master
    '''
    while True:
        try:
            s.connect((HOST, PORT))
            break
        except:
            pass

    while True:
        msg = { 'cmd'           :'READY', 
                'response_to'   :'NULL' 
        }

        s.send(pickle.dumps(msg))
        log('me', 'master', msg)

        ref_msg = { 'cmd'           : 'ACK', 
                    'response_to'   : 'READY'
        }
        msg = pickle.loads(s.recv(1024))
        log('master', 'me', msg)

        if msg == ref_msg:
            return True

        time.sleep(1)

def receive_start_request():
    '''
    '''
    while True:
        msg = pickle.loads(s.recv(1024))
        log('master', 'me', msg)

        if msg['cmd'] == 'PLAY':
            seek_to         = msg['seek_to']
            scheduled_time  = msg['scheduled_time']

            # Call video player to start
            os.system('omxplayer omx_test/test.mp4')

            msg = {'cmd': 'ACK', 'response_to': 'PLAY'}
            s.send(pickle.dumps(msg))
            
            log('me', 'user', 'Initiating video player...')

            return True



def main():
    ''' Main task flow for client
    '''

    try:
        while True:
            init()

            receive_start_request()

            # wait()

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

if __name__ == "__main__":
    preload()
    main()