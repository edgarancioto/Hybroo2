import os
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)

cors = CORS(app, resource={r"/*":{"origins": "*"}})

@app.route("/", methods=['GET'])
def index():
    return "<h1>HYBROO!</h1>"

@app.route('/functions')
def functions():
    function_names = json.load(open(os.path.dirname(__file__) + "/BackEnd/FunctionProblem/Functions/functions-names.json"))
    #function_names = json.load(open(os.path.dirname(__file__) + "/" + os.pardir + "/BackEnd/FunctionProblem/Functions/functions.json"))
    return function_names


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()