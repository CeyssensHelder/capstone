from flask import Flask, request, jsonify, send_from_directory
from model import model_train, model_predict, model_load
import numpy as np
import re
import os
import argparse

app = Flask(__name__)

@app.route('/train', methods=['GET', 'POST'])
def train():
    # Check for request data
    if not request.json:
        return jsonify({"message": "No request data found"}), 400
    
    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True
    
    print("... training model")
    model = model_train(data_dir="data/cs-train", test=test)
    print("... training complete")

    return jsonify({"message": "Training successful"}), 200

@app.route('/predict', methods=['GET','POST'])
def predict():
    # Implement your prediction logic here

    # check input
    if not request.json:
        return jsonify({"message": "No request data found"}), 400
    if 'query' not in request.json:
        return jsonify({"message": "No query data found"}), 400
    if 'type' not in request.json:
        return jsonify({"message": "No type data found"}), 400
    
    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True

    query = request.json['query']

    if request.json['type'] == 'dict':
        pass
    else:
        return jsonify({"message": "Unknown query type"}), 400
    
    model = model_load()

    if not model:
        return jsonify({"message": "Model not found"}), 400
    
    # the model_predict function expects a country, year, month, day, model and test flag
    # we can get these from the query
    country = query['country']
    year = query['year']
    month = query['month']
    day = query['day']

    # we can now use the model to predict on this data
    _result = model_predict(country, year, month, day, test=test)
    result={}

    # convert
    for k,v in _result.items():
        if isinstance(v, np.ndarray):
            result[k] = v.tolist()
        else:
            result[k] = v
    
    if not request.data:
        return jsonify({"message": "No query data found"}), 400

    return jsonify(result), 200

@app.route('/logs/<filename>',methods=['GET'])
def logs(filename):
    if not re.search(".log",filename):
        return jsonify({"message": "That file is not available"}), 400
    
    log_dir = os.path.join(".","logs")
    if not os.path.exists(log_dir):
        return jsonify({"message": "No logs found"}), 400
    
    file_path = os.path.join(log_dir,filename)
    if not os.path.exists(file_path):
        return jsonify({"message": "That file is not available"}), 400
    
    return send_from_directory(log_dir, filename, as_attachment=True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test successful"}), 200

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="debug flask")
    args = vars(ap.parse_args())

    if args["debug"]:
        app.run(debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', threaded=True, port=5000)