
import json

from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)

socket_app = SocketIO(app)

@socket_app.on('connected')
def handle_id(data):
    print("Receiving data")
    print(data)
    data_recv = json.loads(data)
    brd_cast = data_recv["move"]
    x = {"sid": data_recv["sid"], "move": brd_cast}
    x_json = json.dumps(x)
    socket_app.emit("server response",x_json, broadcast=True)

if __name__ == '__main__':
    socket_app.run(app, debug=True, host='127.0.0.1', port=3000)
