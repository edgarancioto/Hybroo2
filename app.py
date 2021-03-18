from CODE.OBJECTS import FUNCTION, INSTANCE
from CODE.METHODS import EXECUTION_CONTROL
from sympy import latex, sympify
import os
import json
import asyncio
import websockets

connected = set()

def functions_names():
    file_data = open("./CODE/JSON/functions-names.json", 'r')
    return json.loads(file_data.read())

def functions_details(params):
    function_id = int(params['function_id'])
    try:
        i, _ = find_function_by_id(function_id)
        return i
    except:
        return "<h1>NOT FOUND</h1>"

def functions_details_img(params):
    function_id = int(params['function_id'])
    try:
        i, obj = find_function_by_id(function_id)
        return {
            'id': i['id'],
            'img': ('http://latex.codecogs.com/svg.latex?'+obj.get_format_expression()).replace(' ','')
        }    
    except:
        return "<h1>NOT FOUND</h1>"

def functions_methods():
    file_data = open(os.path.dirname(__file__) + "./CODE/JSON/functions-methods.json", 'r')
    return json.loads(file_data.read())

def functions_solver(params): 
    function_id = int(params['function_id'])
    isHybrid = bool(params['isHybrid'])
    _, function_obj = find_function_by_id(function_id)
    function_obj.set_n_dimension(int(params['dimension']))
    return EXECUTION_CONTROL.execute_control(function_obj, isHybrid, params)

def find_function_by_id(id):
    file_data = open("./CODE/JSON/functions-details.json", 'r')
    data = json.loads(file_data.read())
    for i in data['data']:
        if id == i['id']:
            function_selected_object = FUNCTION.Function()
            function_selected_object.build_function(i)
            return i, function_selected_object
    raise Exception("Index out of bounds")

def call_tasks(string):
    task = globals()[string['task']]
    if string['params'] == 'None':
        return json.dumps(task())
    return json.dumps(task(string['params']))


async def server(websocket, path):
    connected.add(websocket) 
    try:
        async for message in websocket:
            message = json.loads(message)
            for conn in connected:
                if conn == websocket:
                    await conn.send(call_tasks(message))
    finally:
        connected.remove(websocket)

port = int(os.environ.get("PORT", 5000))
start_server = websockets.serve(server, "0.0.0.0", port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()