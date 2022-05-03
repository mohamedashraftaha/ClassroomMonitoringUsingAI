import flask
from flask import Flask, request
from flask_cors import cross_origin
import subprocess
from subprocess import Popen, PIPE, STDOUT
import requests
import json

iterator = 0
process = None
app = Flask(__name__)
@app.route('/runmodel/<sensitivity>/<exam_instance_id>', methods = ['POST', 'GET'])
def runmodel(sensitivity,  exam_instance_id):

    if request.method == 'POST':
        error_msg = None
        global process
        process = subprocess.Popen(["python3","-u","main.py","-s", f"{sensitivity}", "-e", f"{exam_instance_id}"], stdout= PIPE)
        return 'Model Started Successfully\n'
    return 'Finished'


@app.route('/debugmodel', methods = ['POST', 'GET'])
def debugmodel():

    if request.method == 'GET':
        error_msg = None
        global process
        print(process.stderr)
        for line in process.stdout:
            print(line.decode().rstrip())   
            if process.stderr != None:
                error_msg = process.stderr
                print(error_msg)
                break
        return str(error_msg)
    return 'Finished'
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')