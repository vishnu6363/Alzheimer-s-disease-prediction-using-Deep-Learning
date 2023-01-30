from flask import Flask,flash,render_template,request,redirect,session,url_for
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import urllib.request
from werkzeug.utils import secure_filename
import sys
import glob
import re
import os
import uuid
import urllib
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import mysql.connector
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image




conn=mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12594101",password="e9ZAv7jekG",database="sql12594101")
mycursor=conn.cursor()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'convolutional_2D.h5'))


ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT




def predict(filename , model):
    img  = tf.keras.preprocessing.image.load_img(filename,
                                                 #seed=123,
                                                 target_size=(128,128),
                                                 # #batch_size=64 )
    )
    test_data=image.img_to_array(img)
    img=np.expand_dims(test_data,axis=0)
    prediction = model.predict(img)
    class_names = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']
    pred = np.argmax(prediction, axis=1)
    return pred





app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if "id" in session:
         return render_template('register.html')
    else:
        return redirect('/') 

    


@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static\\images')
    if request.method == 'POST':
        if (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename

                prediction = predict(img_path , model)               

            else:
                error = "Please upload images of jpg , jpeg and png extension only"

            if(prediction[0] == 0):
                return  render_template('new_result.html' )
            elif(prediction[0] == 1):
                return  render_template('mod.html' )
            elif(prediction[0] == 2):
                return  render_template('non.html' )
            elif(prediction[0] == 3):
                return  render_template('very.html' )

    else:
        return render_template('home.html')
    



@app.route('/perform_registration',methods=['POST'])
def perform_registration():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
       
    
    params = [email]
    count = mycursor.execute('select * from login where email=%s', params)  
    user_info = mycursor.fetchall() 
    if len(user_info)>0:
        return render_template('register.html',message="Gmail is already exist")
        
        
    else:        
        mycursor.execute("INSERT INTO `login`(`id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')".format(name,email,password))
        conn.commit()
        return render_template('register.html',message="Registered Successfully")

    



@app.route('/login_val',methods=['POST'])
def login_val():
    email = request.form.get('email')
    password = request.form.get('password')
    mycursor.execute("SELECT * FROM `login` WHERE `email` LIKE '{}' AND `password` LIKE '{}'".format(email,password))
    result=mycursor.fetchall()
    L=len(result)
    if L>0:
        return render_template('home.html')
    else:               
        return render_template('login.html',message="incorrect email/password")
    
    
 
    
    
    



app.run(debug=True)

