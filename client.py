from svideo import *

s = None 

def preload():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def init():
    s.connect((HOST, PORT))
    while True:
        msg = { 'cmd'           :'READY', 
                'response_to'   :'NULL' 
        }

        s.send(pickle.dumps(msg))
        log('me', 'master', msg)

        msg = pickle.loads(s.recv(1024))
        log('master', 'me', msg)

        time.sleep(1)

def main():
    try:
        while True:
            init()

    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

if __name__ == "__main__":
    preload()
    main()