import socketio
import requests

sio = socketio.AsyncServer()
app = socketio.WSGIApp(sio)

MOCKOON_API_URL = "http://mockoon-service/api/test"

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def my_event(sid, data):
    print(f"Received event from {sid}: {data}")
    response = requests.get(MOCKOON_API_URL)
    await sio.emit('my_response', response.json(), room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
