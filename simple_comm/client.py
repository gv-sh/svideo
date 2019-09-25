import asyncio
import websockets

port = 8765
host = 'localhost'

async def simple():
    uri = 'ws://' + host + ':' + str(port)
    async with websockets.connect(uri) as websocket:
        data = input('Enter data to send:')

        await websocket.send(data)
        print('Data sent.')

        ack = await websocket.recv()
        print(ack)

def main():
    asyncio.get_event_loop().run_until_complete(simple())

if __name__ == "__main__":
    main()