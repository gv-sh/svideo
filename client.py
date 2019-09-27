from svideo import *

client_socket = None 
do_not_connect_flag = False

def preload():
    ''' Setup socket to communicate with server '''

    # Using global client_socket for initializing a TCP/IP socket
    # This socket will be used across this program as client to another server program
    global client_socket

    # Creating an IPV4 socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket to be reusable
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Configure maximum listening time for socket calls
    # The socket will not block main program execution for not more than this time
    # Uncomment below to set time out
    # server_socket.settimeout(LISTENING_TIME_OUT)


def init():
    ''' Send READY status to server '''

    # Keep trying to connect until connected to server
    while True:
        try:
            client_socket.connect((HOST, PORT))
            do_not_connect_flag = True
            break
        except:
            pass

    # Once connected, send READY message to server
    # Break from the function when receive ACK from server
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
    ''' Receive instructions to start the video'''
    
    # Wait to receive play instructions
    while True:
        msg = pickle.loads(s.recv(1024))
        log('master', 'me', msg)

        if msg['cmd'] == 'PLAY':
            seek_to         = msg['seek_to']
            scheduled_time  = msg['scheduled_time']

            log('me', 'user', 'Initiating video player...')

            # Call video player to start
            os.system('omxplayer omx_test/test.mp4')

            # Send to server that video is started
            msg = {'cmd': 'ACK', 'response_to': 'PLAY'}
            client_socket.send(pickle.dumps(msg))
            
            return True



def main():
    ''' Main task flow for client'''

    try:
        while True:

            # Send READY to server
            init()

            # Play video on server's message
            receive_start_request()

            # wait()

    # Graceful shutdown
    except KeyboardInterrupt:
        s.close()
        sys.exit(0)


if __name__ == "__main__":
    preload()
    main()