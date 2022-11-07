from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import numpy as np
import pickle
from datetime import datetime

app = Flask(__name__)

model = pickle.load(open('My_featured_disease_model.pkl', 'rb')) 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'heart'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/about")
def aboutus():
    return render_template('about.html')

@app.route('/contactus')
def contact():
    return render_template('contact.html')

@app.route('/predictm')
def predict():
    return render_template('Heart Disease Classifier.html')

@app.route('/predictm', methods =['POST','GET'])
def predictm():
    features = []
    cp = request.form.get("cp")
    features.append(cp)
    thal = request.form.get("thal")
    features.append(thal)
    ca = request.form.get("ca")
    features.append(ca)
    exang = request.form.get("exang")
    features.append(exang)
    sex = request.form.get("sex")
    features.append(sex)
    oldpeak = request.form.get("oldpeak")
    features.append(oldpeak)

    patient = []
    name = request.form.get("name")
    patient.append(name)
    Email = request.form.get("emailid")
    patient.append(Email)
    Mobile = request.form.get("mo")
    patient.append(Mobile)

    now = datetime.now()
    cdt = now.strftime("%d/%m/%Y %H:%M:%S")
    patient.append(cdt)

    cursor = mysql.connection.cursor() 
    usql = "INSERT INTO `data`(`cp`, `thal`, `ca`, `exang`, `sex`, `name`, `mobile`, `email`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (cp, thal, ca, exang, sex, name, Mobile, Email)
    cursor.execute(usql, values)
    mysql.connection.commit()
    cursor.close()

    array_features = [np.array(features)]
    prediction = model.predict(array_features)
    output = prediction

    if output == 1:
        return render_template('positive.html',rvalue=features,p=patient)
    elif output == 0:  
        return render_template('negative.html',rvalue=features,p=patient)



if __name__ == '__main__':
#Run the application
    app.debug=True
    app.run(host='localhost', port=3000)