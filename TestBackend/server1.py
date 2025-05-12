# backend1.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Server 1"

app.run(port=5001)
