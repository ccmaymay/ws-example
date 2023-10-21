from flask import Flask, render_template
from flask_socketio import SocketIO
import json
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return r'''
<!doctype html>
<html lang=en>
  <head>
    <title>WS</title>
  </head>
  <body>
    <script src="https://cdn.socket.io/4.6.0/socket.io.min.js" integrity="sha384-c79GN5VsunZvi+Q/WObgk2in0CbZsHnjEqvFxC5DxHn9lTfNce2WW6h2pH6u/kF+" crossorigin="anonymous"></script>
    <script type="text/javascript">
      const socket = io();
      socket.on('connect', () => {console.log("connect"); console.log(socket);});
      socket.on('message', (message) => {console.log("message"); console.log(message); socket.send(message);});
      socket.on('json', (data) => {console.log("json"); console.log(data); socket.emit('json', data);});
      socket.on('my response', (data) => {console.log("my response"); console.log(data); socket.emit('my event', data);});
    </script>
  </body>
</html>
'''

@socketio.on('connect')
def test_connect():
    socketio.send('Hello WebSocket')

@socketio.on('message')
def handle_message(message):
    sleep(1)
    socketio.send({'Message': message}, json=True)

@socketio.on('json')
def handle_json(data):
    sleep(1)
    socketio.emit('my response', {'JSON': data})

@socketio.on('my event')
def handle_my_custom_event(data):
    sleep(1)
    socketio.send('My event: ' + str(json.dumps(data)))

@socketio.on_error()
def error_handler(e):
    print(f'***ERROR*** {e}')

if __name__ == '__main__':
    socketio.run(app, port=8088)
