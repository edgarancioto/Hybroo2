from CODE.OBJECTS import FUNCTION, INSTANCE
from CODE.METHODS import EXECUTION_CONTROL
from sympy import latex, sympify
import os
import json
import asyncio
import websockets

connected = set()

opc = 1

def functions_names():
    global opc
    print(opc)
    if opc == 1:
        opc = 2
        return try_opc("../HYBROO2/CODE/JSON/functions-names.json")
    if opc == 2:
        opc = 3
        return try_opc("../CODE/JSON/functions-names.json")
    if opc == 3:
        opc = 4
        return try_opc("/CODE/JSON/functions-names.json")
    if opc == 4:
        opc = 1
        return try_opc("./CODE/JSON/functions-names.json")
    

def try_opc(string):
    try:
        file_data = open(string, 'r')
        return json.loads(file_data.read())
    except FileNotFoundError:
        return string

async def server(websocket, path):
    connected.add(websocket) 
    try:
        async for message in websocket:
            for conn in connected:
                if conn == websocket:
                    await conn.send(json.dumps(globals()[message]()))
    finally:
        connected.remove(websocket)

port = int(os.environ.get("PORT", 5000))
start_server = websockets.serve(server, "0.0.0.0", port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()