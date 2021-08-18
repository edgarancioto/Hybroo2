from CODE.OBJECTS import FUNCTION
from CODE.METHODS import EXECUTION_CONTROL
from sympy import latex
import os
import json
import asyncio
import websockets

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Main():

    sender_address = 'hybrooh@gmail.com'
    sender_pass = 'hybroo@01'

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
        j = {}

        simulation = int(params['collectionData']['simulation'])
        
        if simulation == 0:
            await conn.send(json.dumps({'data':'Starts a single execution', 'task':'functions_solver'}))
            j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.solve_functions, params['collectionData'])
            j['task'] = 'functions_solver_results'
            await conn.send(json.dumps(j))
            return {'data':'Finishing the execution', 'task':'functions_solver'}
        
        await conn.send(json.dumps({'data':'Starts a new Simulation', 'task':'simule_functions'}))
        j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.simule_functions, params['collectionData'], simulation)
        j['task'] = 'simule_functions_results'
        await conn.send(json.dumps(j))
        return {'data':'Finishing the simulation', 'task':'simule_functions'}


    @classmethod
    async def instances_names(cls, conn):
        data = {}
        data['task'] = 'instances_names'
        for folder in os.listdir('./CODE/INSTANCES/'):
            data[folder] = os.listdir('./CODE/INSTANCES/'+folder)
        return json.loads(json.dumps(data))

    @classmethod
    async def instances_methods(cls, conn):
        j = json.loads(open(os.path.dirname(__file__) + "./CODE/JSON/instances-methods.json", 'r').read())
        j['task'] = 'instances_methods'
        return j

    @classmethod
    async def instances_solver(cls, conn, params):
        j = {}

        simulation = int(params['collectionData']['simulation'])
        if simulation == 0:
            await conn.send(json.dumps({'data':'Starts a new execution', 'task':'instances_solver'}))
            j['task'] = 'instances_solver_results'
            j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.solve_instances, params['collectionData'])
            await conn.send(json.dumps(j))
            return {'data':'Finishing the execution', 'task':'instances_solver'}
        
        await conn.send(json.dumps({'data':'Starts a new simulation', 'task':'simule_instances'}))
        j['task'] = 'simule_instances_results'
        j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.simule_instances, params['collectionData'], simulation)
        await conn.send(json.dumps(j))
        return {'data':'Finishing the simulation', 'task':'simule_instances'}
    
    @classmethod
    async def send_email(cls, conn, params):
        mail_content = """Hello"""
        receiver_address = 'junior.ancioto@gmail.com'
        message = MIMEMultipart()
        message['From'] = cls.sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by Python. It has an attachment.'
        message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(cls.sender_address, cls.sender_pass)
        text = message.as_string()
        session.sendmail(cls.sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')


if __name__ == "__main__":
    Main().run()
    
    """data = {'collectionData': {
        "problem":"2", "dimension":"2",
        "isHybrid":False,
        "firstMethod":{
        "name-method":"ga",
        "Population":"50",
        "Generation":"3",
        "Crossover":"0.8",
        "Mutation":"0.05",
        "Elitism":"0.15"},
        "secondMethod":{
        "name-method":"0"}}}

    j = {}
    j['data'] = EXECUTION_CONTROL.simule_functions(data['collectionData'], 10)
    print(j)
    """
    """
    data = {'collectionData': {
        "problem":"A-n32-k5.vrp",
        "isHybrid":True,
        "firstMethod":{
            "name-method":"vrp-ga",
            "Population":"50",
            "Generation":"3",
            #"Crossover":"0.8",
            #"Simple":"0.04",
            "Inverse":"0.08",
            "Elitism":"0.15",
            "Special":"checked"
        },
        "secondMethod":{
            "name-method":"vrp-ga",
            "Population":"50",
            "Generation":"50",
            #"Crossover":"0.8",
            #"Simple":"0.04",
            "Inverse":"0.08",
            "Elitism":"0.15",
            "Special":"checked"
        }}}
    """
    """
    data = {'collectionData': {
        "problem":"A-n32-k5.vrp",
        "isHybrid":False,
        "firstMethod":{
            "name-method":"vrp-ga",
            "Population":"50",
            "Generation":"1000",
            "Inverse":"1",
            "Elitism":"0.2",
            "Special":"checked"
        },"secondMethod":{0}}}
    '''784'''
    j = {}
    j['data'] = EXECUTION_CONTROL.simule_instances(data['collectionData'],3)
    print(j['data']['costs'])
    print(j['data']['times'])
    """
    