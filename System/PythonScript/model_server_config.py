import flask
from flask import Flask
from flask_cors import cross_origin
import subprocess
from subprocess import Popen, PIPE, STDOUT


iterator = 0
app = Flask(__name__)
@app.route('/runmodel/<sensitivity>/<exam_instance_id>')
@cross_origin()
def runmodel(sensitivity,  exam_instance_id):
    error_msg = None
    process = subprocess.Popen(["python3","-u","main.py","-s", f"{sensitivity}", "-e", f"{exam_instance_id}"], stdout= PIPE)
    print(process.stderr)
    for line in process.stdout:
        print(line.decode().rstrip())   
        if process.stderr != None:
            error_msg = process.stderr
            print(error_msg)
            break
    return str(error_msg)
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')