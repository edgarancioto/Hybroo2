from CODE.OBJECTS import FUNCTION, INSTANCE
from CODE.METHODS import EXECUTION_CONTROL
from sympy import latex
import os
import json
import asyncio
import websockets

class Main():

    @classmethod    
    def run(cls):
        cls.connected = []
        cls.port = int(os.environ.get("PORT", 5000))
        cls.start_server = websockets.serve(cls.server, "0.0.0.0", cls.port)
        cls.loop = asyncio.get_event_loop()
        cls.loop.run_until_complete(cls.start_server)
        cls.loop.run_forever()
    
    @classmethod
    async def server(cls, websocket, path):
        cls.connected.append(websocket)
        try:
            async for message in websocket:
                message = json.loads(message)
                for conn in cls.connected:
                    if conn == websocket:
                        await conn.send(await cls.call_tasks(conn, message))
        finally:
            cls.connected.remove(websocket)
    
    @classmethod
    async def call_tasks(cls, conn, string):
        print('Test on call_tasks')
        print(string)
        task = getattr(cls, string['task'])
        if string['params'] == 'None':
            return json.dumps(await task(conn))
        return json.dumps(await task(conn, string['params']))

    @classmethod
    def find_function_by_id(cls, id):
        data = json.loads(open("./CODE/JSON/functions-details.json", 'r').read())
        for i in data['data']:
            if id == i['id']:
                function_selected_object = FUNCTION.Function()
                function_selected_object.build_function(i)
                return i, function_selected_object
        raise Exception("Index out of bounds")

    @classmethod
    async def home_info(cls, conn):
        j = json.loads(open("./CODE/JSON/home-page.json", 'r', encoding='utf-8').read())
        j['task'] = 'home_info'
        return j

    @classmethod
    async def functions_names(cls, conn):
        j = json.loads(open("./CODE/JSON/functions-names.json", 'r').read())
        j['task'] = 'functions_names'
        return j

    @classmethod
    async def functions_details(cls, conn, params):
        try:
            i, _ = Main.find_function_by_id(int(params['function_id']))
            i['task'] = 'functions_details'
            return i
        except:
            return "<h1>NOT FOUND</h1>"

    @classmethod
    async def functions_details_img(cls, conn, params):
        try:
            i, obj = Main.find_function_by_id(int(params['function_id']))
            return { 'id': i['id'],'task': 'functions_details_img', 'img': ('http://latex.codecogs.com/svg.latex?'+obj.get_format_expression()).replace(' ','')}    
        except:
            return "<h1>NOT FOUND</h1>"

    @classmethod
    async def functions_methods(cls, conn):
        j = json.loads(open(os.path.dirname(__file__) + "./CODE/JSON/functions-methods.json", 'r').read())
        j['task'] = 'functions_methods'
        return j

    @classmethod
    async def functions_solver(cls, conn, params):
        params = params['collectionData']
        isHybrid = bool(params['isHybrid'])

        _, function_obj = cls.find_function_by_id(int(params['problem']))
        
        await conn.send(json.dumps({'data':'Starts a new execution', 'task':'functions_solver'}))
        j = {}
        j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.execute_function, function_obj, isHybrid, params)
        j['task'] = 'functions_solver_results'
        await conn.send(json.dumps(j))
        return {'data':'Finishing the execution', 'task':'functions_solver'}

    @classmethod
    async def instances_names(cls, conn):
        data = {}
        data['task'] = 'instances_names'
        for folder in os.listdir('./CODE/INSTANCES/'):
            data[folder] = os.listdir('./CODE/INSTANCES/'+folder)
        return json.loads(data)

    @classmethod
    async def instances_methods(cls, conn):
        j = json.loads(open(os.path.dirname(__file__) + "./CODE/JSON/instances-methods.json", 'r').read())
        j['task'] = 'instances_methods'
        return j

    @classmethod
    async def instances_solver(cls, conn, params):
        params = params['collectionData']
        isHybrid = bool(params['isHybrid'])
        _, function_obj = cls.find_function_by_id(int(params['problem']))
        if function_obj.multidimensional:
            function_obj.set_n_dimension(int(params['dimension']))
        await conn.send(json.dumps({'data':'Starts a new execution', 'task':'functions_solver'}))
        j = {}
        j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.execute_control, function_obj, isHybrid, params)
        j['task'] = 'functions_solver_results'
        await conn.send(json.dumps(j))
        return {'data':'Finishing the execution', 'task':'functions_solver'}


if __name__ == "__main__":
    Main().run()