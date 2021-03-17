from CODE.OBJECTS import FUNCTION, INSTANCE
from CODE.METHODS import EXECUTION_CONTROL
from sympy import latex, sympify
import os
import json
import asyncio
import websockets

connected = set()

def functions_names():
    file_data = open(os.path.dirname(__file__) + "/CODE/JSON/functions-names.json", 'r')
    return json.loads(file_data.read())

async def server(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn == websocket:
                    await conn.send(json.dumps(globals()[message]()))
    finally:
        connected.remove(websocket)
        
start_server = websockets.serve(server, "0.0.0.0", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()