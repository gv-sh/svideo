from svideo import *


server_socket   = None
clients         = []
READY           = False


def preload():
    ''' Create and bind socket '''

    # Using global server_socket for initializing a TCP/IP socket
    # This socket will be used across this program as server
    global server_socket

    # Creating an IPV4 socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket to be reusable
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Configure maximum listening time for socket calls
    # The socket will not block main program execution for not more than this time
    server_socket.settimeout(LISTENING_TIME_OUT)

    # Bind socket to given host address and port number
    server_socket.bind((HOST, PORT))

    # Maximum number of queued connections possible to this socket
    server_socket.listen(MAX_CLIENTS)

    return


def is_not_connected(client_address):
    ''' Checks if client is still not connected to master '''

    global clients

    # Check for the new client in the already connected list of clients
    for client in clients:
        if client_address == client['addr']:
            return False
    
    # Return True only if not found in the existing list
    # Note that this function is checking if a client is not in the list
    return True


def wait_for_ready(client_socket, client_address):
    ''' Wait for confirmation from client's for READY status '''
    
    global clients

    # Start with checking if the client is not already connected
    if is_not_connected(client_address):  

        # Read data from client and deserialize into dictionary
        # Each data msg between svideo server and client is sent as 
        # serialized dictionary using pickle
        msg = pickle.loads(client_socket.recv(1024))

        # Logging every communication between server, client and user
        # User is the person who might be watching server or client's
        # command line interface
        log(client_address, 'master', msg)

        # Check if client is in READY state
        if msg['cmd'] == 'READY': 

            # Append client info to clients variable for further comm.
            clients.append({'socket': client_socket, 'addr': client_address})

            # Compose ACK message
            msg = { 'cmd'           : 'ACK', 
                    'response_to'   : 'READY'
            }

            # Send serialized ACK message to client
            client_socket.send(pickle.dumps(msg))
            
            # Print comm. log
            log('master', client_address, msg)


def request_playback(client, seek_to, scheduled_time):
    ''' Request client to start the video from seek_to seconds at the scheduled_time '''

    # Get client socket
    client_socket = client['socket']

    # Compose PLAY message
    msg = { 'cmd'           : 'PLAY', 
            'seek_to'       : seek_to,
            'scheduled_time': scheduled_time
    }
    
    # Send PLAY message to client
    client_socket.send(pickle.dumps(msg))

    # Print comm. log
    log('master', client['addr'], msg)


def init():
    ''' Wait for all connections '''

    # Run until all clients are up
    while len(clients) < MAX_CLIENTS :

        # Wrapped the below in try block to avoid accept() blocking the
        # main program beyond MAX_CLIENTS
        try:
            # Load client socket and address after accepting new connection
            client_socket, client_address = server_socket.accept()
        
        # Come here when there is no calls from client after time out period
        except socket.timeout:

            # Re-attempt waiting for new connections if all clients are not up
            continue

        # Compose a run a thread to handle clients to see if they are READY
        T = threading.Thread(target = wait_for_ready, args=(client_socket, client_address))
        T.start()   


def start_all():
    ''' Request all the clients to begin video '''

    # Set a scheduled time to start all the videos
    scheduled_start_time = datetime.datetime.now() + datetime.timedelta(seconds=60)

    # Send playback requests to all the videos
    for c in clients:
        request_playback(c, 0, scheduled_start_time)



def show_client_count():
    ''' For testing only. Show number of concurrent clients '''

    while True:
        print('client count:' + str(len(clients)))
        time.sleep(0.5)


def main():
    ''' Task flow for server '''

    # Uncomment the following code to show periodic client count 
    # T = threading.Thread(target = show_client_count, args=())
    # T.start()

    log('master', 'user', 'Initiating svideo...')
    
    try:
        # Initialize by listening from all the clients
        init()

        log('master', 'user', 'All clients READY')
        
        # Request all clients to play video
        start_all()

    # Graceful shutdown
    except KeyboardInterrupt:
        s.close()
        sys.exit(0)


if __name__ == "__main__":
    preload()
    main()