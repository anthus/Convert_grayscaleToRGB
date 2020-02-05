from flask import Flask , render_template, redirect, url_for, session
from flask_pymongo import PyMongo
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import subprocess
import time
from flask.helpers import flash
from Execute import main_Execute
from VideoTagGenerator import distinct_tag
from VideoTagGenerator import make_tag

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ConvertGrayscaleToRgb"
mongo = PyMongo(app)
app.secret_key = "ali12345"

@app.route('/')
def index():
    if session.get('username') != None:
        username = session['username']["username"]
        user = mongo.db.Users.find_one({"username" : username})
        #Generate video tag to show colorized videos
        first_part, end_part= distinct_tag()
        make_tag(session['username']["username"], first_part, end_part)
        return render_template('indexlogin.html', user = user)
    return render_template('index.html')

@app.route('/register', methods = ['GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def register():
    name = request.form['name']
    username = request.form['user_name']
    email_address = request.form['email_address']
    password = request.form['password']
    checkUser  = {"username" : username}
    user = mongo.db.Users.find_one(checkUser)
    if user:
        return render_template('login.html', message="Your username already existed")
    user_information = {"name" : name, "username" : username, "email_address" : email_address, "password" : password, "validity" : int(100)}
    mongo.db.Users.insert_one(user_information)
    # html = "<center>You have been registered successfully<br/><a href = ""http://localhost:5000"">back to home page</a></center>"
    return render_template('indexlogin.html', user = user_information)

@app.route('/checklogin', methods = ['POST'] ) 
def checklogin():
    user_name = request.form['user_name']
    password = request.form['password']
    checkUser  = {"username" : user_name, "password" : password}
    user = mongo.db.Users.find_one(checkUser, {"_id":0})
    if user:   
        session['username'] = user
        #Generate video tag to show colorized videos
        first_part, end_part= distinct_tag()
        make_tag(session['username']["username"], first_part, end_part)
        return render_template('indexlogin.html', user = user)
    else:
        html = "<center>Your username or password aren't correct <a href = ""http://localhost:5000"">back</a></center>"
        return html
      
    
@app.route('/profile')
def profile():
    if session['username'] != None:
        username = session['username']["username"]
        user = mongo.db.Users.find_one({"username" : username})
        return render_template('index2.html', user = user) 
    return render_template('index.html')

    
@app.route('/Logout')
def Logout():
      session.pop('username',None)
      return redirect(url_for('index'))

@app.route('/process' , methods = ['POST' ,'GET'] )
def Upload():
    if session.get('username') != None:
        if request.method == 'POST':
            if request.files.get('file', None):
                if int(request.form['val']) >= 0:
                    session['username']['validity'] = request.form['val']
                    mongo.db.Users.update({"username": session['username']["username"]}, {"$set":{"validity" : request.form['val']}})
                    #upload file to video directory
                    uploads_dir = (r"video")
                    filmName = "GrayscaleVideo.mp4"
                    grayvideo = request.files['file']
                    grayvideo.save(os.path.join(uploads_dir, secure_filename(filmName)))
                    #Execute VideoColorizer.py
                    main_Execute(session['username']["username"], session['username']['validity'])
            else:
                flash('Please load a file', 'warning')
    return redirect(url_for('index'))
    


if __name__ == "__main__":
    app.run(debug=True)

