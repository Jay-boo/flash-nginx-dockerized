from flask import Flask, jsonify
import pandas as pd
import json
import boto3
import pickle
import numpy as np

app = Flask(__name__)

def convert_JSON_to_df(JSONdict,asArray:bool=True):
    df=pd.read_json(json.dumps(JSONdict))
    if asArray : pd.DataFrame.to_numpy(df)
    return df


def download_file_from_s3():
    boto3.setup_default_session(profile_name='jayBisBis')
    s3 = boto3.client("s3")
    s3.download_file(
        Bucket="testbucketja-new-houston",
        Key="logr.pkl",
        Filename="downloaded_from_s3.pkl"
    )
    print("pkl file downloaded")





def load_mod(filename:str="downloaded_from_s3.pkl"):
    mod=pickle.load(open(filename,'rb'))
    return mod

def prediction(mod,X_test):
    return mod.predict(X_test)

def job(JSONdict,asArray:bool=True):
    df=convert_JSON_to_df(JSONdict)
    return prediction(load_mod(),df)

##########################################################



@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, HOUSTON!'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    res=job(data)
    print(res)
    print(list(res))
    res=list(res)
    myDict=dict(zip([i for i in range(len(res))],res))
    return ({'result':json.dumps(myDict)})

@app.route('/square', methods=['POST'])
def square():
    data = request.get_json()
    num = data['number']
    result = num ** 2
    return jsonify({'result': result})

if __name__ == "__main__":
    download_file_from_s3()
