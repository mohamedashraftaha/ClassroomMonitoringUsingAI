import flask
from flask import Flask
from flask_cors import cross_origin
import subprocess
app = Flask(__name__)
@app.route('/runmodel/<sensitivity>/<exam_instance_id>')
@cross_origin()
def runmodel(sensitivity,  exam_instance_id):
    process = subprocess.Popen(["python3","test.py","-s", f"{sensitivity}", "-e", f"{exam_instance_id}"], stdout= subprocess.PIPE)
    x = process.communicate()[0]
    return x.decode()
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')