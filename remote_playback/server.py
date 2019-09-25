import asyncio
import websockets

port = 8765
host = 'localhost'

# making a change
async def simple(websocket, path):
    data = await websocket.recv()
    print('Data received: ' + data)

    ack = 'Data received by server.'

    await websocket.send(ack)
    print('Acknowledgement sent to client')

def main():
    start_server = websockets.serve(simple, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
