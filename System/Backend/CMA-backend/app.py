from re import S
from flask import Flask, jsonify,redirect,url_for,render_template,request
import sqlalchemy, json,secrets
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import hashlib, MySQLdb

# configuration of the app
app=Flask(__name__)
app.config.from_pyfile('config.py')


# database configuration using ORM (object relation mapping)
db = SQLAlchemy(app=app) 
Base = automap_base()
Base.prepare(db.engine,reflect=True)

## Tables
ExamRoom = Base.classes.examroom
Admin = Base.classes.adminstrator
cheatingincidents = Base.classes.cheatingincidents
frames = Base.classes.frames
proctor = Base.classes.proctor
examincidents = Base.classes.examIncidents
## important variables
#this variable will be used to store passwords in the DB
salt = None

## error handling
@app.errorhandler(404)
def not_found(error):
    return json.dumps({'status': 'fail', 'message': 'Not found'}), 404

@app.route('/registerAdmin',methods=['POST'])
def registerAdmin():
    
    if request.method == "POST":
        """ @API Description: This API is used to reguister an admininstrator to the system """
        #getting the request parameters
        NationalID = request.form['national_id']
        password = request.form['password']
        FirstName = request.form['first_name']
        LastName = request.form['last_name']
        position = request.form['position']
        if "national_id" not in request.form or "password" not in request.form or "first_name" not in request.form \
            or "last_name" not in request.form or  "position" not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            salt = password + app.config['SECRET_KEY']
            db_pass = hashlib.md5(salt.encode()).hexdigest()
            newAdmin = Admin(NationalID = NationalID, passwd= db_pass, FirstName=FirstName,\
                LastName=LastName, position=position)
            db.session.add(newAdmin)
            db.session.commit()

        except sqlalchemy.exc.IntegrityError as e:
            return json.dumps({'status': 'fail', 'message': "User Already Exists"})

    return json.dumps({'status': 'Success', 'message': "Administrator Added Successfully!"})

@app.route('/registerProctor',methods=['POST'])
def registerProctor():
    
    if request.method == "POST":
        """ @API Description: This API is used to register an invigilator to the system """
        #getting the request parameters
        NationalID = request.form['national_id']
        password = request.form['password']
        FirstName = request.form['first_name']
        LastName = request.form['last_name']
        SchoolName = request.form['school_name']
        if "national_id" not in request.form or "password" not in request.form or "first_name" not in request.form \
            or "last_name" not in request.form or  "school_name" not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            salt = password + app.config['SECRET_KEY']
            db_pass = hashlib.md5(salt.encode()).hexdigest()
            new_proctor = proctor(NationalID = NationalID, passwd= db_pass, FirstName=FirstName,\
                LastName=LastName, SchoolName=SchoolName)
            db.session.add(new_proctor)
            db.session.commit()

        except sqlalchemy.exc.IntegrityError as e:
            print(e.args    )
            return json.dumps({'status': 'fail', 'message': "User Already Exists"})

    return json.dumps({'status': 'Success', 'message': "Administrator Added Successfully!"})


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)
