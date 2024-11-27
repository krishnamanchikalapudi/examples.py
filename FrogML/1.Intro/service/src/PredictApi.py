import time
import inspect, time, datetime, warnings
from datetime import date, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import io
from json import JSONEncoder
import os.path
from os import path

#app = Flask(__name__)
app = Flask(__name__, static_folder='build', static_url_path='/')
app.debug = True
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    method_name = f"{inspect.stack()[0][3]}"
    # print(f" METHOD: {method_name} at {datetime.now()}] ")
    return "Welcome to the JFrog Intro MLOps training session!\n"

@app.route('/predict', methods=['GET', 'POST'])
def getstockinfo():
        today = date.today()
        startDate = today

    