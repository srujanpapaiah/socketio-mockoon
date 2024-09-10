FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install python-socketio aiohttp requests
CMD ["python", "socketio_server.py"]
