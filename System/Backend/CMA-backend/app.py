from flask import Flask, jsonify,redirect,url_for,render_template,request
import sqlalchemy, json,secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


# configuration of the app
app=Flask(__name__)
app.config.from_pyfile('config.py')


# database configuration using ORM (object relation mapping)
db = SQLAlchemy(app=app) 
Base = automap_base()
Base.prepare(db.engine,reflect=True)
ExamRoom = Base.classes.examroom




@app.route('/',methods=['GET','POST'])
def test():
    data = ExamRoom(ExamroomID='12', ExamID='ARIC',SchoolName='AUC')
    db.session.add(data)
    db.session.commit()
    return jsonify('results', 'test')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)
