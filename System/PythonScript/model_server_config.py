import flask
from flask import Flask, request, jsonify
from flask_cors import cross_origin
import subprocess
from subprocess import Popen, PIPE, STDOUT
import requests
import json
import os
import signal

iterator = 0
process = None
app = Flask(__name__)

"""
This python file is repsonsible for the communication between the frontend and the model.
The frontend invoke this API making use of the fact that both the frontend and the model are on the same network, thus the
IP address of the server that runs the DL model is known. We are makng use of the library subprocess, by which the server creates a child process
responsible for running the model. The API below is only responsible for creating this process
"""
@app.route('/runmodel/<sensitivity>/<exam_instance_id>/<vidName>', methods = ['POST', 'GET'])
def runmodel(sensitivity,  exam_instance_id,vidName):
    """
    -- API Description: This API is used for the communication between the frontend and the DL model. It is invoked
    by the frontend
    -- params: sensitivity, exam_instance
    -- return data: msg
    """
    if request.method == 'POST':

        response = requests.get(f"https://classroommonitoring.herokuapp.com/api/user/check_exam_ended/{exam_instance_id}")
        if (response.json()['data'] == "exam ended"):
            return jsonify({'Status': 'this exam instance has ended'}) ,201
        if (response.json()['msg'] == "Exam not found"):
            return jsonify({'Status': 'Exam Not Found'}) ,201
        error_msg = None
        global process
        process = subprocess.Popen(["python3","-u","main.py","-s", f"{sensitivity}", "-e", f"{exam_instance_id}", "-v", f"{vidName}"], stdout= PIPE)
        return 'Model Started Successfully\n'
    return 'Finished'


@app.route('/debugmodel', methods = ['POST', 'GET'])
def debugmodel():

    if request.method == 'GET':
        """
        -- API description: the main advantage of this API is to allow debugging the model and observe the outputs to make sure
        that everything is working correctly
        -- params: N/A
        -- returned data : N/A
        """
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

@app.route('/stopmodel/<string:exam_instance_id>', methods = ['POST'])
def stopmodel(exam_instance_id):

    if request.method == 'POST':
        """
        -- API description: this API is for debugging purposes to stop the process 
        -- params: N/A
        -- returned data : N/A
        """
        global process
        try:
            os.kill(process.pid, signal.SIGINT)
        except AttributeError as e:
            return jsonify({'Status': 'model not running'}) ,201

        
        response = requests.get(f"https://classroommonitoring.herokuapp.com/api/user/end_exam/{exam_instance_id}")
        print(response.json())
        print(response.json()['data'])
        if (response.json()['data'] == "exam ended successfully"):
            return jsonify({'Status': 'exam instance, process killed'}) ,201
        error_msg = None      
          
    return 'proccess killed'
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
