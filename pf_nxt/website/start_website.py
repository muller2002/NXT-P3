from flask import Flask
from flask import render_template
import subprocess
import random
app = Flask(__name__)



@app.route('/')
def hello(name=None):
    lip = getip()
    sid = getSID()
    return render_template('index.html', ip=str(lip), sessionID = str(sid))

def getip():
    ip = subprocess.check_output("hostname -I", shell=True).decode('utf-8') #get ip
    ip = ip[:-2] #eliminate unwanted characters
    return ip
def getSID():
    return random.randint(0, 9223372036854775807)


@app.route('/accelerometer.html')
def accelo():
    sid = getSID()
    return render_template ('accelerometer.html', ip=str(getip()), sessionID = str(sid))


@app.route('/joystick.html')
def joystick():
    sid = getSID()
    return render_template ('joystick.html', ip=str(getip()), sessionID = str(sid))
