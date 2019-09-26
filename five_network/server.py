import asyncio
import websockets

port = 8765
host = 'localhost'
clients = set()

def stateEvent():
    return json.dumps({'type': 'status', **state})

def clientEvent():
    return json.dumps({'type': 'clients', 'counts': len(clients)})

async def notifyState():
    if clients:
        message = stateEvent()
        await asyncio.wait([client.send(message) for client in clients])

async def notifyClients():
    if clients:
        message = clientEvent()
        await asyncio.wait([client.send(message) for client in clients])

async def register(websocket):
    clients.add(websocket)
    await notifyClients() 

async def unregister(websocket):
    clients.remove(websocket)
    await notifyClients()

def main(websocket, path):
    await register(websocket)
    try:
        await websocket.send(stateEvent()))
        async for message in websocket:
            data = json.loads(message)


if __name__ == "__main__":
    start_server = websockets.serve(main, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
