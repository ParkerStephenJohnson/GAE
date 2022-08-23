#push
from flask import Flask, jsonify, render_template, request
import json
import pandas as pd
from google.cloud import bigquery
import os

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'level-research-356200-8abdeae2d5d5.json'

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/data/', methods = ['POST'])
def data():
    if request.method == 'POST':
        form_data = request.form
        
        print(form_data)
        #df = pd.read_json('data/nested_list.json')
        # #dict_train = json.load(form_data)
        # df = pd.DataFrame(list(form_data.items(1)))
        # #,columns = ['age','sex','cp','trestbps','chol','fbs','restcg','thalach','exang','oldpeak','slope','ca','thal']
        # df_T = df.T
        # df_T.columns = ['age','sex','cp','trestbps','chol','fbs','restcg','thalach','exang','oldpeak','slope','ca','thal']
        # print(df)

        # print(df.columns)
        # client = bigquery.Client()
        # #dataset = bigquery.Dataset('level-research-356200.heart_disease')
        # #dataset = client.create_dataset(dataset, timeout=30)
        # dataset_ref = client.dataset('heart_disease')
        # table_ref = dataset_ref.table('input')
        # print(table_ref)
        # client.load_table_from_dataframe(df, table_ref)

        query = """
        ML.PREDICT(MODEL `level-research-356200.heart_disease.heart_random_forest`,
        TABLE `level-research-356200.heart_disease.input`)))
        """

        #query_res = client.query(query)

        # for row in query_res:
        #     print(row)
# converting json dataset from dictionary to dataframe
        #to_predict = pd.DataFrame.from_dict(dict_train, orient='index'))

        prediction = {'prediction':'No Heart Disease'}
        return render_template('data.html',form_data = prediction)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
