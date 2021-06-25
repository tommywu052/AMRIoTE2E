import asyncio
import websockets



CLIENTS = set()

async def broadcast():
    while True:
        for ws in CLIENTS:
            print(ws)
            #async for message in ws:
            #    await ws.send(message)
        await asyncio.sleep(2)

#asyncio.get_event_loop().create_task(broadcast())

async def echo(websocket, path):
    print('echo')
    while True:
        CLIENTS.add(websocket)
        
        #try :
            #for ws in CLIENTS:
        if CLIENTS:
            need_update = await websocket.recv()
            print("Need Update flag=======")
            print(need_update)
            message = need_update            
            await asyncio.wait([user.send(message) for user in CLIENTS])

header = {'Connection': 'Upgrade'}
asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 13000, extra_headers=header))
asyncio.get_event_loop().run_forever()