import time
from locust import HttpUser, task, between
import socketio

class SocketIOUser(HttpUser):
    wait_time = between(1, 3)
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = socketio.Client()
        self.client.on('connect', self.on_connect)
        self.client.on('my_response', self.on_my_response)
        self.client.on('disconnect', self.on_disconnect)

    def on_connect(self):
        print(f"User {self.client.sid} connected")

    def on_my_response(self, data):
        print(f"Received response: {data}")
        self.environment.events.request_success.fire(
            request_type="socketio",
            name="my_response",
            response_time=int((time.time() - self.start_time) * 1000),
            response_length=len(str(data))
        )

    def on_disconnect(self):
        print(f"User {self.client.sid} disconnected")

    def on_start(self):
        self.client.connect('http://localhost:5000')

    def on_stop(self):
        self.client.disconnect()

    @task
    def send_event(self):
        self.start_time = time.time()
        self.client.emit('my_event', {'message': 'Hello Server!'})

class SocketIOLoadTest(SocketIOUser):
    host = "http://localhost:5000"

    @task
    def perform_socketio_test(self):
        self.send_event()
        time.sleep(1)