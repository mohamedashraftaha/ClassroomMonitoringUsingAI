from re import S
import re
from flask import Flask, jsonify,redirect, session,url_for,render_template,request
import sqlalchemy, json,secrets
from flask_sqlalchemy import SQLAlchemy
import boto3
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
import hashlib, MySQLdb
from userDefinedExceptions import *
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
proctorExamAssignment = Base.classes.proctor_adminstrator_assign
## important variables
#this variable will be used to store passwords in the DB
salt = None

##############################################################

"""Admin-level APIs"""    

#########################################################

@app.route('/registerAdmin',methods=['POST'])
def registerAdmin():
    """ @API Description: This API is used to reguister an admininstrator to the system """
    if request.method == "POST":
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
##############################################################
@app.route('/loginAdmin',methods=['POST'])
def loginAdmin():
    """ @API Description: This API is used to login an admininstrator to the system """  
    if request.method == "POST":
        #getting the request parameters
        NationalID = request.form['national_id']
        password = request.form['password']
        if "national_id" not in request.form or "password" not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            salt = password + app.config['SECRET_KEY']
            db_pass = hashlib.md5(salt.encode()).hexdigest()
            user =db.session.query(Admin).filter_by(NationalID=NationalID).first()
            if user is None:
                raise NotFound
            if db_pass != user.passwd:
                raise NotFound
        except NotFound:
            return json.dumps({'status': 'fail', 'message': "User Not Found"})
        except sqlalchemy.exc.IntegrityError as e:
            return json.dumps({'status': 'fail', 'message': "User Already Exists"})

    return json.dumps({'status': 'Success', 'message': "Admin logged in successfully!"})

#########################################################
@app.route('/createExamInstance', methods=['POST'])
def createExamInstance():
    if request.method == "POST":
        #getting the request parameters
        ExamRoomID = request.form['examroom_id']
        ExamID = request.form['exam_id']
        SchoolName = request.form['school_name']
        adminNatID = request.form['admin_national_id']
        if "examroom_id" not in request.form or "exam_id" not in request.form or "school_name" not in request.form\
            or "admin_national_id" not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            
            # admin not found
            user =db.session.query(Admin).filter_by(NationalID=adminNatID).first()
            if user is None:
                raise NotFound
            
            # else admin is found
            newRoom = ExamRoom(ExamroomID = ExamRoomID, ExamID= ExamID, SchoolName=SchoolName,\
                admin_national_id = adminNatID)
            db.session.add(newRoom)
            db.session.commit()
        except NotFound:
            return json.dumps({'status': 'fail', 'message': "Admin Not Found"})
        except sqlalchemy.exc.IntegrityError as e:
            return json.dumps({'status': 'fail', 'message': "exam instance Already Exists"})

    return json.dumps({'status': 'Success', 'message': "exam instance created Successfully!"})
    
##############################################################
@app.route('/proctorExamAssignment', methods=['POST'])
def assignproctor_to_exam():
    if request.method == "POST":
        #getting the request parameters
        adminNatID = request.form['admin_national_id']
        proctorNatID = request.form['proctor_national_id']
        AssignedExamRoomID = request.form['exam_room_id']
        if "admin_national_id" not in request.form or "proctor_national_id" not in request.form or "exam_room_id" not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            
            # admin not found
            a =db.session.query(Admin).filter_by(NationalID=adminNatID).first()
            if a is None:
                raise NotFound
            
             # admin not found
            p =db.session.query(proctor).filter_by(NationalID=proctorNatID).first()
            if p is None:
                raise NotFound
            
             # admin not found
            eid =db.session.query(ExamRoom).filter_by(ExamroomID=AssignedExamRoomID).first()
            if eid is None:
                raise NotFound
            
            # else admin is found
            newAssignment = proctorExamAssignment(admin_national_id = adminNatID, proctor_national_id= proctorNatID, \
                AssignedExamRoomID = AssignedExamRoomID)
            db.session.add(newAssignment)
            db.session.commit()
        except NotFound:
            return json.dumps({'status': 'fail', 'message': "Admin or Proctor or Exam Room ID Not Found"})
        except sqlalchemy.exc.IntegrityError as e:
            return json.dumps({'status': 'fail', 'message': "Assignment Already Exists"})

    return json.dumps({'status': 'Success', 'message': "Assignment Completed Successfully!"})
    
###############################################################

"""user-level APIs"""

################################################################
@app.route('/registerProctor',methods=['POST'])
def registerProctor():
    """ @API Description: This API is used to register an invigilator to the system """
    if request.method == "POST":
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

    return json.dumps({'status': 'Success', 'message': "Proctor Added Successfully!"})

######################################################################
@app.route('/loginProctor',methods=['POST'])
def loginProctor():
    """ @API Description: This API is used to login an Proctor to the system """
    if request.method == "POST":
        #getting the request parameters
        NationalID = request.form['national_id']
        password = request.form['password']
        if "national_id" not in request.form or "password" not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            salt = password + app.config['SECRET_KEY']
            db_pass = hashlib.md5(salt.encode()).hexdigest()
            user =db.session.query(proctor).filter_by(NationalID=NationalID).first()
            if user is None:
                raise NotFound
            if db_pass != user.passwd:
                raise NotFound
        except NotFound:
            return json.dumps({'status': 'fail', 'message': "User Not Found"})
        except sqlalchemy.exc.IntegrityError as e:
            return json.dumps({'status': 'fail', 'message': "User Already Exists"})

    return json.dumps({'status': 'Success', 'message': "Proctor logged in successfully!"})
######################################################################
@app.route('/CreateIncident',methods=['POST'])
def CreateIncident():
    """ @API Description: This API is used to CreateIncident """
    
    if request.method == "POST":
        #getting the request parameters
        ExamRoomID = request.form['examroom_id']
        state = request.form['stat']
        if  "stat" not in request.form or "examroom_id"not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
           erid = db.session.query(ExamRoom).filter_by(ExamroomID= ExamRoomID)
           if erid is None:
                raise NotFound
           newincident=examincidents(stat=state, ExamroomID= ExamRoomID)
           db.session.add(newincident)
           db.session.commit()
        except NotFound:
            return json.dumps({'status': 'fail', 'message': "Invalid!"})
        except sqlalchemy.exc.IntegrityError as e:
            print(e.args)
            return json.dumps({'status': 'fail', 'message': "Incident Already Exists or not found"})

    return json.dumps({'status': 'Success', 'message': "Incident Completed Successfully!"})
######################################
@app.route('/AddIncidentframes',methods=['POST'])
def AddIncidentframes():
    """ @API Description: This API is used to add frames """
    
    if request.method == "POST":
        #getting the request parameters
        IncidentID = request.form['IncidentID']
        
        if  IncidentID not in request.form:
                return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
        try:
            client=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
            for file in os.listdir():
                if '.jpg' in file:
                    bucket='classroommonitoring'
                    bucket_file_path='jpg/'+str(file)
                    client.upload_file(file,bucket,bucket_file_path)  
        except NotFound:
            return json.dumps({'status': 'fail', 'message': "Invalid!"})
        except sqlalchemy.exc.IntegrityError as e:
            print(e.args)
            return json.dumps({'status': 'fail', 'message': "Incident Already Exists or not found"})

    return json.dumps({'status': 'Success', 'message': "Incident Completed Successfully!"})
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)
