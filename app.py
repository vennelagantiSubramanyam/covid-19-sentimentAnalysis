from flask import Flask, render_template, request, jsonify, session
from retrieve_tweet import data_collection,download_user,download_user_bulk
import joblib
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import tweepy 
import requests
from textblob import TextBlob
import matplotlib
matplotlib.rcParams['text.color'] ='tab:orange'
from analisis_data_profil import preprocess, preprocess_bulk
import pickle
 

app = Flask(__name__)


tfidf = pickle.load(open('tfidf.pkl','rb'))

svm = pickle.load(open('decision.pkl','rb'))


app.secret_key = 'twitter'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

#SESSION_TYPE = 'filesystem'

 


def prediction_bulk(df):
    skrip = preprocess_bulk(df)
    pred_proba=model.predict_proba(skrip)
    y_pred=model.predict(skrip)
    percentage=pred_proba[:,1]
    joins=' '.join(map(str, percentage))
    perc=float(joins)*100
    percent=(str(perc)+"%")
    #print(y_pred)
    df = df.drop(df.columns[[17,18,19,20,21,22]], axis = 1)
    return df,percent,y_pred

def prediction(df):
    skrip,tab = preprocess(df)
    pred_proba=model.predict_proba(skrip)
    y_pred=model.predict(skrip)
    percentage=pred_proba[:,1]
    joins=' '.join(map(str, percentage))
    perc=float(joins)*100
    percent=perc
    print(y_pred)
    return percent,tab,y_pred
    
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/collect")
def collect():
    df = data_collection()
    df=df.sort_values(by=['username']).reset_index(drop=True)
    df.to_csv('collect.csv') 
    return render_template('collect.html',df=df.to_html())
@app.route("/prediction")
def prediction():
    df = data_collection()
    df=df.sort_values(by=['username']).reset_index(drop=True)
    df.to_csv('collect.csv')
        
    return render_template('prediction.html',df=df.to_html())

@app.route('/senti', methods=['GET', 'POST'])
def senti():
	if request.method=='POST':
		word = request.form['senti_word']
		#pt = api.search(word)
		analysis = TextBlob(word)
		sentiment = analysis.sentiment.polarity
		if sentiment > 0:
			ans = 'Positive Statement'
		elif sentiment < 0:
			ans = 'Negative Statement'
		else:
			ans = 'Neutral Statement'
		return render_template('result.html', word = word, ans = ans, sentiment = sentiment)
	return render_template('prediction.html')    
@app.route('/predictions')
def predictions():
 	return render_template("predictions.html")

#@app.route('/chart')
#def chart():
	#abc = request.args.get('news')	
	#input_data = [abc.rstrip()]
	# transforming input
	#tfidf_test = tfidf_vectorizer.transform(input_data)
	# predicting the input
	#y_pred = pac.predict(tfidf_test)
    #output=y_pred[0]
	#return render_template('chart.html', prediction_text='Review is {}'.format(y_pred[0])) 

@app.route('/results')
def results():	

	abc = request.args.get('check')	
	input_data = [abc.rstrip()]
	# transforming input
	tfidf_test = tfidf.transform(input_data)
	# predicting the input
	y_pred = svm.predict(tfidf_test) 
	return render_template('predictions.html', prediction_text=y_pred[0])     
    
@app.route('/performance')
def performance():
 	return render_template("performance.html")

@app.route('/chart')
def chart():
 	return render_template("chart.html")    
   
if __name__ == "__main__":
    app.run()   

