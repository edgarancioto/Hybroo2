import os
from flask import Flask, request
from flask_cors import CORS
import json
from sympy import latex, sympify

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins": "*"}})

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
    file_data = open(os.path.dirname(__file__) + "/BackEnd/FunctionProblem/Functions/functions-details.json", 'r')
    data = json.loads(file_data.read())
    for i in data['data']:
        if function_id == i['id']:
            return i
    return "<h1>NOT FOUND</h1>"


@app.route('/functions-details-img')
def functions_details_img():
    function_id = int(request.args.get('id'))
    file_data = open(os.path.dirname(__file__) + "/BackEnd/FunctionProblem/Functions/functions-details.json", 'r')
    data = json.loads(file_data.read())
    for i in data['data']:
        if function_id == i['id']:
            func = sympify(i['formulation'], evaluate=False)
            return 'http://latex.codecogs.com/svg.latex?'+latex(func)
    return "<h1>NOT FOUND</h1>"
        


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()