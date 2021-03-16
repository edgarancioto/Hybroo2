from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/functions-names')
def api():
    print('api()')
    sys.stdout.flush()
    query = dict(request.args)
    emit('edgar', 'dict(data=str(query))', broadcast=True)
    return jsonify(dict(success=True, message='Received'))


@socketio.on('my event')
def on_connect():
    print('on_connect()')
    payload = dict(data='Connected')
    emit('edgar', payload, broadcast=True)


@socketio.on("message")
def handleMessage(data):
    print('a')
    emit("new_message",data,broadcast=True)

if __name__ == '__main__':
    print('main')
    socketio.run(app, debug=True)