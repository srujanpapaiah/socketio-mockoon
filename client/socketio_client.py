import socketio

sio = socketio.Client()

@sio.event
def connect():
    
    print("Connected to server")
    sio.emit('my_event', {'message': 'Hello Server!'})

@sio.event
def my_response(data):
    print(f"Received response: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")

sio.connect('http://localhost:5000')
sio.wait()
