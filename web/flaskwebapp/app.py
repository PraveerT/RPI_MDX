# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request,Response,session,g
import os
import picamera 
import cv2
import time 
import socket 
import io
from camera import Camera
# create the application object
app = Flask(__name__)
app.secret_key = os.urandom(24)
# use decorators to link the function to a url











#-----------------------------------


def gen(camera):
    while True:
        frame = camera.get_frame()
        print ("frame")
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#-----------------------------------

@app.route('/', methods=['GET', 'POST'])
def home():

    error = None
    if request.method == 'POST':
        session.pop('user',None)
        if request.form['username'] == 'iot' and request.form['password'] == 'iotstation':
            session['user']=request.form['username']
            return redirect(url_for('dashboard'))

    return render_template('welcome.html', error=error)
# start the server with the 'run()' method

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return 'Logout successful'



@app.route('/welcome')
def welcome():

    return render_template('welcome.html')  # render a template

@app.route('/dashboard')
def dashboard():
    if g.user:


        return render_template('dashboard.html')  # render a template
    if request.method == 'POST':
        dropsession()

    return redirect(url_for('home'))


@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']
    # Route for handling the login page logic
# Route for handling the login page logic

       
@app.route('/video_feed') 
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(Camera()), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 
if __name__ == '__main__': 
	app.run(host='10.230.127.35',port=55555, debug=True, threaded=True) 

