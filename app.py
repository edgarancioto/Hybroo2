from CODE.OBJECTS import FUNCTION
from CODE.METHODS import EXECUTION_CONTROL
from sympy import latex
import os
import json
import asyncio
import websockets
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
                        await cls.call_tasks(conn, message)
        finally:
            cls.connected.remove(websocket)
    
    @classmethod
    async def call_tasks(cls, conn, string):
        print('\nTest on call_tasks', string)
        
        task = getattr(cls, string['task'])
        if string['params'] == 'None':
            await task(conn)
        else:
            await task(conn, string['params'])

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
        await conn.send(json.dumps(j))

    @classmethod
    async def functions_names(cls, conn):
        j = json.loads(open("./CODE/JSON/functions-names.json", 'r').read())
        j['task'] = 'functions_names'
        await conn.send(json.dumps(j))

    @classmethod
    async def functions_details(cls, conn, params):
        try:
            j, _ = Main.find_function_by_id(int(params['function_id']))
            j['task'] = 'functions_details'
        except:
            j = "<h1>NOT FOUND</h1>"
        await conn.send(json.dumps(j))

    @classmethod
    async def functions_details_img(cls, conn, params):
        try:
            i, obj = Main.find_function_by_id(int(params['function_id']))
            j = { 'id': i['id'],'task': 'functions_details_img', 'img': ('http://latex.codecogs.com/svg.latex?'+obj.get_format_expression()).replace(' ','')}    
        except:
            j =  "<h1>NOT FOUND</h1>"
        await conn.send(json.dumps(j))

    @classmethod
    async def functions_methods(cls, conn):
        j = json.loads(open(os.path.dirname(__file__) + "./CODE/JSON/functions-methods.json", 'r').read())
        j['task'] = 'functions_methods'
        await conn.send(json.dumps(j))

    @classmethod
    async def functions_solver(cls, conn, params):
        j = {}
        simulation = int(params['collectionData']['simulation'])
        
        if simulation == 0:
            j['task'] = 'functions_solver'
            j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.solve_functions, params['collectionData'])
            await conn.send(json.dumps(j))
        else:
            j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.simule_functions, params['collectionData'], simulation)
            await cls.send_simulation(conn, params, j)
        

    @classmethod
    async def instances_names(cls, conn):
        j = {}
        j['task'] = 'instances_names'
        for folder in os.listdir('./CODE/INSTANCES/'):
            j[folder] = os.listdir('./CODE/INSTANCES/'+folder)
        await conn.send(json.dumps(j))

    @classmethod
    async def instances_methods(cls, conn):
        j = json.loads(open(os.path.dirname(__file__) + "./CODE/JSON/instances-methods.json", 'r').read())
        j['task'] = 'instances_methods'
        await conn.send(json.dumps(j))

    @classmethod
    async def instances_solver(cls, conn, params):
        j = {}
        simulation = int(params['collectionData']['simulation'])

        if simulation == 0:
            j['task'] = 'instances_solver'
            j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.solve_instances, params['collectionData'])
        else:
            j['data'] = await cls.loop.run_in_executor(None, EXECUTION_CONTROL.simule_instances, params['collectionData'], simulation)
            await cls.send_simulation(conn, params, j)
    
    @classmethod
    async def send_simulation(cls, conn, params, results):
        params['results'] = results

        json_file = io.StringIO(json.dumps(params['collectionData']))

        mail_content = 'Some description text about Hybroo'
        receiver_address = params['collectionData']['userMail']
        message = MIMEMultipart()
        message['From'] = cls.sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A first version of mail with simulation results.'
        
        message.attach(MIMEText(mail_content, 'plain'))
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(json_file.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment', filename='simulation.json')
        message.attach(payload)
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(cls.sender_address, cls.sender_pass)
        text = message.as_string()
        session.sendmail(cls.sender_address, receiver_address, text)
        session.quit()


if __name__ == "__main__":
    Main().run()
    