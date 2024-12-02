import inspect, time
import json
import pandas as pd
from xgboost import XGBClassifier

from flask import Flask, request, jsonify
#from flask_cors import CORS

import json
import io
from json import JSONEncoder
import os.path
from os import path
import xgboost as xgb

#app = Flask(__name__)
app = Flask(__name__, static_folder='build', static_url_path='/')
app.debug = True
#CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    method_name = f"{inspect.stack()[0][3]}"
    # print(f" METHOD: {method_name} at {datetime.now()}] ")
    resp="Welcome to the JFrog Intro MLOps training session!"
    # return resp
    return jsonify(result=resp)

@app.route('/predict', methods=['POST'])
def getPredict():
    returnVal = None
    startTime = time.perf_counter()
    try:
        data = request.get_json()
        df = pd.DataFrame(data)

        # load the model
        model = xgb.XGBClassifier()
        model.load_model("churn_model.bin")
        predictions = model.predict_proba(df)[:, 1]  # Get probabilities for "churn"
        returnVal = jsonify({"churn_probabilities": predictions.tolist()})
        print("Return churn probabilities: ", returnVal)

    except Exception as err:
        print("Error: ", str(err))

    totalTime = (time.perf_counter() - startTime)
    print(f"process completed in {format(totalTime, '6.3f')} seconds or {format(totalTime / 60, '6.3f')} minutes")  
    return returnVal

@app.errorhandler(404)
def service_not_found(error):
    return jsonify(result="NO Service available")

# if __name__ == '__main__':
#     app.run(debug=True)
#     app.run(host='0.0.0.0', port=5000)
    