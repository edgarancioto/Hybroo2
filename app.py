import os
from flask import Flask, request, send_file
from flask_cors import CORS
import json
from sympy import latex, sympify
from BackEnd.FunctionProblem import FUNCTION

app = Flask(__name__)
cors = CORS(app, resource={r"/*":{"origins": "*"}})

function_selected_object = None


@app.route("/", methods=['GET'])
def index():
    return "<h1>HYBROO!</h1>"

@app.route('/functions-names')
def functions_names():
    file_data = open(os.path.dirname(__file__) + "/BackEnd/FunctionProblem/Functions/functions-names.json", 'r')
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
    function_id = int(request.args.get('id'))
    try:
        i, _ = find_function_by_id(function_id)
        return {
            'id': i['id'],
            'img': ('http://latex.codecogs.com/png.latex?'+function_selected_object.get_format_expression()).replace(' ','')
        }
    except:
        return "<h1>NOT FOUND</h1>"

def find_function_by_id(id):
    global function_selected_object
    file_data = open(os.path.dirname(__file__) + "/BackEnd/FunctionProblem/Functions/functions-details.json", 'r')
    data = json.loads(file_data.read())
    for i in data['data']:
        if id == i['id']:
            if function_selected_object is None or function_selected_object.id != i['id'] :
                function_selected_object = FUNCTION.Function()
                function_selected_object.build_function(i)
            return i, function_selected_object
    raise Exception("Index out of bounds")



def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()