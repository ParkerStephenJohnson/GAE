#push
from flask import Flask, jsonify, render_template, request
import json
import pandas as pd
from google.cloud import bigquery
import os

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'level-research-356200-8abdeae2d5d5.json'

@app.route('/')
def homepage():
    return render_template('form.html')

@app.route('/api', methods=['POST'])
def form():
    if request.method == 'POST':
       # print(type(request.get_json()))
        response_dict = request.get_json()
        df = pd.DataFrame([response_dict])

        client = bigquery.Client()

        query = f"""
        SELECT
        *
        FROM
        ML.PREDICT(MODEL `heart_disease.heart_random_forest`,
            (
            SELECT
            {df.iloc[0]['age']} AS age, '{df.iloc[0]['sex']}' as sex, {df.iloc[0]['cp']} as cp, {df.iloc[0]['trestbps']} as trestbps
        ,   {df.iloc[0]['chol']} as chol, {df.iloc[0]['fbs']} as fbs, {df.iloc[0]['restecg']} as restecg, {df.iloc[0]['thalach']} as thalach, {df.iloc[0]['exang']} as exang
        ,   {df.iloc[0]['oldpeak']} as oldpeak, {df.iloc[0]['slope']} as slope, {df.iloc[0]['ca']} as ca, {df.iloc[0]['thal']} as thal)
        )
        """

        job = client.query(query)
        result = pd.DataFrame([row for row in job.result()])

        prediction = {'prediction':result[0][0]['predicted_target']}

        return prediction

@app.route('/data/', methods = ['GET','POST'])
def data():
    if request.method == 'POST':
        form_data = request.form
        
        df = pd.DataFrame(list(form_data.items(1)))
        df_T = df.T
        df_T.columns = ['age','sex','cp','trestbps','chol','fbs','restcg','thalach','exang','oldpeak','slope','ca','thal']

        client = bigquery.Client()

        query = f"""
        SELECT
        *
        FROM
        ML.PREDICT(MODEL `heart_disease.heart_random_forest`,
            (
            SELECT
            {df.iloc[0][1]} AS age, '{df.iloc[1][1]}' as sex, {df.iloc[2][1]} as cp, {df.iloc[3][1]} as trestbps
        ,   {df.iloc[4][1]} as chol, {df.iloc[5][1]} as fbs, {df.iloc[6][1]} as restecg, {df.iloc[7][1]} as thalach, {df.iloc[8][1]} as exang
        ,   {df.iloc[9][1]} as oldpeak, {df.iloc[10][1]} as slope, {df.iloc[11][1]} as ca, {df.iloc[12][1]} as thal)
        )
        """

        job = client.query(query)
        result = pd.DataFrame([row for row in job.result()])

        prediction = {'prediction':result[0][0]['predicted_target']}

        return render_template('data.html',form_data = prediction)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
