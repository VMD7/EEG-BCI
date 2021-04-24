from flask import Flask,redirect,render_template,url_for,request,jsonify
import pandas as pd
import numpy as np
import pickle


app = Flask(__name__, template_folder="template")
with open("Models/best_gbc.pickle", 'rb') as data:
    model = pickle.load(data)

@app.route("/",methods=['GET'])
def home():
	return render_template("index.html")


@app.route('/eegpredict', methods=['GET', 'POST'])
def eegpredict():
    title = 'EEG - Emotion Analysis'
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return render_template('predictor.html', title=title)
        try:
            files = request.files["file"]
            df = pd.read_csv(files)
            pred = model.predict([df.iloc[0]])
            if pred== 0:
                predict = "Negative"
                return render_template('Negative_Prediction.html', prediction=predict,title=title)
            elif pred==1:
                predict = "Neutral"
                return render_template('Neutral_Prediction.html', prediction=predict,title=title)
            elif pred==2:
                predict = "Positive"
                return render_template('Positive_Prediction.html', prediction=predict,title=title)
            print(files)
            return render_template('Negative_Prediction.html', prediction=pred[0],title=title)
        except:
            pass
    return render_template('predictor.html', title=title)
    

if __name__ == '__main__':
    app.run(debug=False)