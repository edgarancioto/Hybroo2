from CODE.OBJECTS import FUNCTION, INSTANCE
from CODE.METHODS import EXECUTION_CONTROL

from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from sympy import latex, sympify

import os
import json
"""
#cors = CORS(app, resource={r"/*":{"origins": "*"}})

@socketio.on('my event')
def handle_my_custom_event():
    print('received json: ')


@app.route("/", methods=['GET'])
def index():
    return "<h1>HYBROO !</h1>"

@app.route('/functions-names')
def functions_names():
    file_data = open(os.path.dirname(__file__) + "/CODE/JSON/functions-names.json", 'r')
    return json.loads(file_data.read())

@app.route('/functions-details')
def functions_details():
    function_id = int(request.args.get('id'))
    try:
        i, _ = find_function_by_id(function_id)
        return i
    except:
        return "<h1>NOT FOUND</h1>"

@app.route('/functions-details-img')
def functions_details_img():
    try:
        function_id = int(request.args.get('id'))
        i, obj = find_function_by_id(function_id)
        return {
            'id': i['id'],
            'img': ('http://latex.codecogs.com/svg.latex?'+obj.get_format_expression()).replace(' ','')
        }    
    except:
        return "<h1>NOT FOUND</h1>"
    
@app.route('/functions-methods')
def functions_methods():
    file_data = open(os.path.dirname(__file__) + "/CODE/JSON/functions-methods.json", 'r')
    return json.loads(file_data.read())

@app.route('/functions-solver', methods = ['POST'])
def functions_solver(): 
    data_post = request.get_json()
    function_id = int(data_post['problem'])
    isHybrid = bool(data_post['isHybrid'])
    _, function_obj = find_function_by_id(function_id)
    function_obj.set_n_dimension(int(data_post['dimension']))
    return EXECUTION_CONTROL.execute_control(function_obj, isHybrid, data_post)

# Extras
def find_function_by_id(id):
    file_data = open(os.path.dirname(__file__) + "/CODE/JSON/functions-details.json", 'r')
    data = json.loads(file_data.read())
    for i in data['data']:
        if id == i['id']:
            function_selected_object = FUNCTION.Function()
            function_selected_object.build_function(i)
            return i, function_selected_object
    raise Exception("Index out of bounds")

################## INSTANCES #####################
@app.route('/instances-names')
def instances_names():
    files_cvrp = [os.path.basename(x) for x in os.listdir(os.path.dirname(__file__) + "/CODE/INSTANCES/CVRP")]
    files_tsp = [os.path.basename(x) for x in os.listdir(os.path.dirname(__file__) + "/CODE/INSTANCES/TSP")]
    names = {
        'cvrp':{},
        'tsp':{}
    }
    j = 1
    for i in files_cvrp:
        names['cvrp'][j] = i
        j += 1
    j = 0
    for i in files_tsp:
        names['tsp'][j] = i
        j += 1
    return names

@app.route('/instances-details')
def instances_details():
    try:
        instance_name = request.args.get('name')
        instance = INSTANCE.Instance()
        instance.load_instance(instance_name)
        return instance.json()
    except:
        return "<h1>NOT FOUND</h1>"
   

@app.route('/instances-details-coord')
def instances_details_coord():
    try:
        instance_name = request.args.get('name').replace('.vrp','-coords.png').replace('.tsp','-coords.png')
        return send_file(os.path.dirname(__file__) + "/CODE/IMAGES/COORD/"+instance_name)
    except:
        return "<h1>NOT FOUND</h1>"


@app.route('/instances-details-best')
def instances_details_best():
    try:
        instance_name = request.args.get('name').replace('.vrp','-best.png').replace('.tsp','-best.png')
        return send_file(os.path.dirname(__file__) + "/CODE/IMAGES/BEST/"+instance_name)
    except:
        return "<h1>NOT FOUND</h1>"


@app.route('/instances-methods')
def instances_methods():
    file_data = open(os.path.dirname(__file__) + "/CODE/JSON/instances-methods.json", 'r')
    return json.loads(file_data.read())


def main():
    port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port, debug=True)
    print(1)
    socketio.run(app,host="0.0.0.0", port=port)
    print(2)


if __name__ == "__main__":
    main()"""

    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('functions-names')
def functions_names(a):
    print("func-name", a['data'])
    file_data = open(os.path.dirname(__file__) + "/CODE/JSON/functions-names.json", 'r')
    emit('response', {'data': json.loads(file_data.read())})
   
@socketio.event
def my_event(message):
    emit('my_response', {'data': 'got it!'})

@socketio.on('messages')
def message(a):
    print('Message from client: ', a)
    my_event('response')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=True)

