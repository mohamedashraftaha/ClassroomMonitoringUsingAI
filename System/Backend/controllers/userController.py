# imports all dependencies
from urllib import response
from app import *
from . import *
#######################
"""
User-level APIs
@description:
This file contains the implementation of all the user level APIs

All of our APIs return status, msg & data
status: success or failed
msg: representing the reason for failure or success
data(if any): data requested by the user 

"""    
#######################
class UserLevelAPIs:

        @userNamespace.route('/login_proctor')
        class login_proctor(Resource):
            
            LoginProctorData = api.model ("LoginProctorData",{'national_id':fields.String(""),\
                'password':fields.String("")})
            @api.doc(body=LoginProctorData,security='apikey')
            def post(self):
                """ 
                -- API Description: This API is used to login an Proctor to the system 
                -- params: national id , password
                -- return data: status, msg, data(if any)
                """            
                status = None
                msg = None
                responseData = None
                try:   
                    data = request.json
                    NationalID = data['national_id']
                    password = data['password']
                    # hash the entered password using our salt to make sure that the comparison
                    # with the password stored in the database is valid
                    salt = password + app.config['SECRET_KEY']
                    db_pass = hashlib.md5(salt.encode()).hexdigest()
                    
                    # check that user is found
                    user =db.classroom_monitoring_db.session.query(db.proctor).filter_by(national_id=NationalID).first()
                    if user is None:
                        status = 'failed'
                        msg= "User Not Found"
                        raise NotFound
                    # check that the passwords match
                    if db_pass != user.passwd:
                        status = 'failed'
                        msg = "incorrect username or password"
                        raise NotFound
                    status = 'success'
                    msg = "Proctor logged in successfully!"
                except KeyError:
                    status = 'failed'
                    msg= 'Missing Parameter'
                    json.loads(json.dumps({'status': status, 'msg': msg, 'data':responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data':responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg= "User Already Exists"
                    return json.loads(json.dumps({'status': status, 'msg':msg, 'data': responseData}))
              
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
# ######################################################################
        @userNamespace.route('/create_possible_case')
        class create_possible_case(Resource):
            CreateIncidentData = api.model ("CreateIncidentData",{'case_id':fields.Integer(),'exam_instance_id':fields.String(""),\
                'student_number':fields.Integer(), 'confidence': fields.Float()})
            @api.doc(body=CreateIncidentData,security='apikey')
            def post(self):
                """ 
                -- API Description: This API is used by the deep learning model to create a possible cheating case based
                on how confident the model is. The status of the case will be defaulted to "pending" until the proctor decides
                -- params: case id, exam instance id, stat, confidence, student number
                -- return: msg, status, responseData(if any)
                """                        
                status = None
                msg = None
                responseData = None
                try:   
                    data = request.json
                    case_id = data['case_id']
                    examInstanceID = data['exam_instance_id']   
                    confidence = data['confidence']   
                    student_number = data['student_number']       
                    # check if exam exists
                    erid = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id= examInstanceID).first()
                    #check if student number is valid
                    snum = db.classroom_monitoring_db.session.query(db.students_positions).filter_by(student_number=student_number).first()
                    if erid is None:
                        status = 'failed'
                        msg = 'exam incident does not exist'
                        raise NotFound
                    
                    if snum is None:
                        status = 'failed'
                        msg = 'student number does not exist'
                        raise NotFound
                    
                    
                    newincident=db.exam_instance_cases(case_id=case_id,stat="pending", exam_instance_id= examInstanceID, confidence = confidence, \
                        student_number=student_number)
                    db.classroom_monitoring_db.session.add(newincident)
                    db.classroom_monitoring_db.session.commit()
                    status = 'success'
                    msg = 'incident completed successfully!'
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    print(e)
                    status = 'failed'
                    msg = 'Incident Already Exists or not found'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except:
                    db.classroom_monitoring_db.session.rollback()
                    raise
                finally:
                     db.classroom_monitoring_db.session.close()
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
#######################################
        @userNamespace.route('/dismiss_case')
        class dismiss_case(Resource):
            dismissData = api.model ("dismissData",{'case_id':fields.String(""), 'exam_instance_id': fields.String("examX")})
            @api.doc(body=dismissData,security='apikey')
            def post(self):
                """ 
                -- API Description: This API is used to update status of the case that
                was recently chearing to Not cheating. i.e: the proctor thinks that this case is a 
                normal case and the student is not cheating
                -- parameters: case id
                --return data: status, msg, response data
                """
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json        
                    caseID = data['caseID'] 
                    exam_instance_id = data['exam_instance_id']
                    # check if exam exists
                    erid = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id= exam_instance_id).first()
                    if erid is None:
                        status = 'failed'
                        msg = 'exam incident does not exist'
                        raise NotFound
                   
                    # check if there exists a case with this id
                    case = db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter(and_(db.exam_instance_cases.exam_instance_id==exam_instance_id,db.exam_instance_cases.case_id==caseID)).first()
                    if case is None:
                        status = 'failed'
                        msg = 'case id not found'
                        raise NotFound
                    # update the status of the case to be not cheating
                    db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter(and_(db.exam_instance_cases.exam_instance_id==exam_instance_id,db.exam_instance_cases.case_id==caseID)).\
                    update({'stat':'NC'})
                    db.classroom_monitoring_db.session.commit()                   
                    status = 'success'
                    msg = 'Case Dismissed Successfully'
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'Process of dismissing the case failed!'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
##########################################################
        @userNamespace.route('/report_case')
        class report_case(Resource):
            reportCaseData = api.model ("reportCaseData",{'caseID':fields.String(""),'exam_instance_id': fields.String("examX")})
            @api.doc(body=reportCaseData,security='apikey')
            def post(self):
                """
                -- API Description: This API is used to update status of the case that
                was recently chearing to  cheating. i.e: the proctor thinks that this case is a 
                normal case and the student is not cheating
                -- parameters: case id
                --return data: status, msg, response data
                """
                #getting the request parameters
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json            
                    caseID = data['caseID'] 
                    exam_instance_id = data['exam_instance_id']    
                    
                    # check if the exam instance entered is valid               
                    erid = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id= exam_instance_id).first()
                    if erid is None:
                        status = 'failed'
                        msg = 'exam incident does not exist'
                        raise NotFound
                   
                   # check if there is a case with this id
                    case = db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter(and_(db.exam_instance_cases.exam_instance_id==exam_instance_id,db.exam_instance_cases.case_id==caseID)).first()
        
                    if case is None:
                        status = 'failed'
                        msg = 'case id not found'
                        raise NotFound 
                     # update the status of the case to be cheating
                    db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter(and_(db.exam_instance_cases.exam_instance_id==exam_instance_id,db.exam_instance_cases.case_id==caseID)).\
                    update({'stat':'C'})
                    db.classroom_monitoring_db.session.commit()
                    status = 'success'
                    msg = 'Case Reported Successfully'
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'       
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except NotFound:

                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:     
                    status = 'failed'
                    msg = 'Process of reporting the case failed!'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except:
                    db.classroom_monitoring_db.session.rollback()
                    raise
                finally:
                     db.classroom_monitoring_db.session.close()
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
################################################################

        @userNamespace.route('/get_frames_links/<int:caseID>/<string:exam_instance_id>/<int:student_number>')
        class get_frames_links(Resource):
            @api.doc(security='apikey')
            @cross_origin()
            def get(self, caseID, exam_instance_id, student_number):
                """
                -- API Description: This API is used to retrieve links of the frames of a given cheating incident. These frames
                are placed in the s3 bucket by the model.
                -- parameters: case id , exam instance 
                -- return data: msg , status, data (list of the frames of the case)
                """
                urlList  = []
                status = None
                msg = None                
                try:
                    '''Connect to the bucket'''
                    client=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,config=Config(region_name = 'eu-north-1'   ,signature_version='s3v4'))
                    session = boto3.Session(aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,                    )
                    bucket='classroommonitoring'
                    s3 = session.resource('s3')
                    mybucket=s3.Bucket(bucket)
                    status = 'success'
                    msg = 'frames retrieved successfully'
                    
                    # check for the exam instance id and the case id
                    checker = db.classroom_monitoring_db.session.query(db.exam_instance_cases).filter(and_(db.exam_instance_cases.case_id== caseID, db.exam_instance_cases.exam_instance_id == exam_instance_id)).first()
                    if checker is None:
                        status = 'failed'
                        msg = 'Case/Exam ID does not Exist'
                        raise NotFound 
                    
                    # get the case name by the convention we specified for the frames in the bucker
                    # convention : c{CaseID}-{exam id}-{student number}
                    cases = f"c{caseID}-{exam_instance_id}-{student_number}"
                    
                    '''Get the frames of the case and add them to the db'''
                    
                    """Check if the requested frame is already in the database"""
                    frame_exist = db.classroom_monitoring_db.session.query(db.frames).filter(and_(db.frames.case_id==caseID, db.frames.exam_instance_id ==exam_instance_id)).first()
                    if frame_exist != None:
                        status = 'success'
                        msg = 'frames retrieved successfully'
                        framsesdata = db.classroom_monitoring_db.session.query(db.frames).filter(and_(db.frames.case_id==caseID, db.frames.exam_instance_id ==exam_instance_id)).first()
                        urlList.append(framsesdata.image_link) 
                        raise NotFound 
                    keys = [i.key for i in mybucket.objects.all()]
                    case_frames = [key for key in keys  if cases in key]
                    for i in range(len(case_frames)):
                        url = client.generate_presigned_url('get_object',Params={ 'Bucket': bucket, 'Key': case_frames[i] }, HttpMethod="GET",ExpiresIn=9800)   
                        urlList.append(url)
                        newframe=db.frames(image_link=url, case_id= caseID, exam_instance_id=exam_instance_id, student_number=student_number)
                        db.classroom_monitoring_db.session.add(newframe)
                        db.classroom_monitoring_db.session.commit()
                    
                    status = 'failed'
                    msg = 'Missing Parameter'  
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))              
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'frames already exists'       
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
                except sqlalchemy.exc.PendingRollbackError as e:     
                    status = 'failed'
                    msg = 'Case ID Does Not exist'      
                    urlList  = None
                    db.classroom_monitoring_db.session.rollback()
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
                except:
                    db.classroom_monitoring_db.session.rollback()
                    raise
                finally:
                     db.classroom_monitoring_db.session.close()
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
################################################################################
        @userNamespace.route('/get_assigned_exams/<string:proctor_national_id>')
        class get_assigned_exams(Resource):
            @api.doc(security='apikey')
            @cross_origin()
            def get(self,proctor_national_id):
                """ 
                -- API Description: This API is used to retrieve all exam instances assigned to the proctor, if any
                -- params: proctor national id
                -- return: status , msg, response data
                """
                status = None
                msg = None
                responseData = None
                try:
                    # search for the assigned exam instances
                    assigned_instances = db.classroom_monitoring_db.session.query(db.admin_assign_proctor).\
                        filter_by(proctor_national_id = proctor_national_id).first()
                    if assigned_instances is None:
                        msg = 'No Assigned Exam Instances to this user'
                        status = 'failed'
                        raise NotFound   
                    responseData = assigned_instances.exam_instance_id
                    msg = 'Exam Instance ID Retrieved Successfully'
                    status = 'success'
                except KeyError:
                    msg = 'No Assigned Exam Instances to this user'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'No Assigned Exam Instances to this user'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except:
                    db.classroom_monitoring_db.session.rollback()
                    raise
                finally:
                     db.classroom_monitoring_db.session.close()
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
#########################################################################
        @userNamespace.route('/assign_model_sensitivity')
        class assign_model_sensitivity(Resource):
            model_sensitivity = api.model ("model_sensitivity",{'proctor_national_id':fields.String(""),\
                'exam_instance_id': fields.String(""), 'model_sensitivity':fields.String("")})
            @api.doc(body=model_sensitivity,security='apikey')
            def post(self):
                """ 
                -- API Description: This API is used to adjust the model sensitivity
                that will be used in the model.
                -- params:  proctor national id , exam instance id, model_sensitivity
                -- return: status, msg, response data
                """
                status = None
                msg = None
                responseData = None
                try:                    
                    data = request.json
                    proctor_national_id = data['proctor_national_id']
                    exam_instance_id = data['exam_instance_id']
                    model_sensitivity = data['model_sensitivity']
                    # search for the assigned exam instances
                    exam_instance = db.classroom_monitoring_db.session.query(db.proctor_monitor_exam).\
                        filter_by(proctor_national_id = proctor_national_id).first()
                        
                    if exam_instance is None:
                        msg = 'no exam instance'
                        status = 'failed'
                        raise NotFound   
                    
                    if exam_instance.exam_instance_id != exam_instance_id:
                        msg = 'No Assigned Exam Instances to this user'
                        status = 'failed'        
                        raise NotFound                   
                    db.classroom_monitoring_db.session.query(db.proctor_monitor_exam).\
                    filter_by(proctor_national_id=proctor_national_id).\
                    update({'model_sensitivity':model_sensitivity})
                    db.classroom_monitoring_db.session.commit()
                    msg = 'Model Sensitivity updated successfully'
                    status = 'success'
                except KeyError:
                    msg = 'No Assigned Exam Instances to this user'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'No Assigned Exam Instances to this user'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except:
                    db.classroom_monitoring_db.session.rollback()
                    raise
                finally:
                     db.classroom_monitoring_db.session.close()
                
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
            
    ############################################################################
        @userNamespace.route('/get_exam_instance_details/<string:examInstanceID>')
        class get_exam_instance_details(Resource):
            @api.doc(security='apikey')
            def get(self, examInstanceID):
                """ -- API Description: This API is used to return all details of an exam instance
                    -- params : exam instance id
                    -- return : status, msg, data-> Exam_Details":[{"Exam_Instance_ID": exam_instance_details.exam_instance_id,\
                            "Exam_Subject_code": exam_instance_details.exam_reference_code,\
                                "School": exam_instance_details.school_name,\
                                    "Assigned_Camera_IP": exam_instance_details.camera_static_ip
                """
                status = None
                msg = None
                responseData = None
                try:                  
                    # check for validity of exam instances
                    exam_instance_details = db.classroom_monitoring_db.session.query(db.exam_instance).\
                        filter_by(exam_instance_id = examInstanceID).first()    
                    if exam_instance_details is None:
                        msg = 'No exam instance found'
                        status = 'failed'
                        raise NotFound           
                    responseData = {"Exam_Details":[{"Exam_Instance_ID": exam_instance_details.exam_instance_id,\
                            "Exam_Subject_code": exam_instance_details.exam_reference_code,\
                                "School": exam_instance_details.school_name,\
                                    "Assigned_Camera_IP": exam_instance_details.camera_static_ip
                    }]}
                   
                    msg = 'Exam Details Retreived successfully'
                    status = 'success'
                except KeyError:
                    msg = 'No Assigned Exam Instances found'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'No Assigned Exam Instances found'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
              
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
            
###########################################################################################
        @userNamespace.route('/add_students_locations')
        class add_students_locations (Resource):
                addStudentsLocations = api.model ("addStudentsLocations",{'student_number':fields.Integer(), 'exam_instance_id': fields.String(""),'x':fields.Float(),\
                    'y':fields.Float(), 'w':fields.Float(),\
                        'h':fields.Float(),})
                @api.doc(body=addStudentsLocations,security='apikey')
                def post(self):
                    """ 
                    -- API Description: This API is used to add students locations based on the bounding boxes generated by YOLO 
                    in the deep learning model
                    -- params: student number, exam instance id, x, y , w , h
                    -- return: msg, status, data
                    """
                    status = None
                    msg = None
                    responseData = None
                    try:  
                        data = request.json
                        student_number = data['student_number']
                        exam_instance_id = data['exam_instance_id']
                        x = data['x']
                        y = data['y']
                        w = data['w']
                        h = data['h']
                        
                        eid =db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                        snum = db.classroom_monitoring_db.session.query(db.students_positions).filter_by(student_number=student_number).first()
                        # check if exam instance exists
                        if eid is None:
                            status = 'failed'
                            msg = 'exam does not exist'
                            raise NotFound
                        # check if there is a student with this number
                        if snum is None:
                            status = 'failed'
                            msg = 'student does not exist'
                            raise NotFound
                         
                        # the defult values of x y w h when admin adds students to 0 0 0 0
                        # but now when we use this api here we will change the values of 0 0 0 0 to the actual x y w h values
                        db.classroom_monitoring_db.session.query(db.students_positions).\
                            filter_by(exam_instance_id=exam_instance_id, student_number=student_number).\
                            update({'x':x, 'y':y,'w':w,'h':h})
                        db.classroom_monitoring_db.session.commit()
                        status = 'success'
                        msg = "Location for student Added Successfully!"
                    except KeyError:
                        status = 'failed'
                        msg = "Missing Parameter"  
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))

                    except NotFound:
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                
                    except sqlalchemy.exc.IntegrityError as e:
                        status = 'failed'
                        msg = "Location Already Exists" 
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))             
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
############################################################################
        @userNamespace.route('/generate_exam_report')
        class generate_exam_report(Resource):
            reportData = api.model ("reportData",{'exam_instance_id':fields.String("")})
            @api.doc(body=reportData,security='apikey')
            def post(self):
                """ 
                -- API Description: This API is used to generate end of exam report of ALL cases either reported or dismissed
                or even pending. i.e: left undecided
                --params: exam instance id
                -- return: status, msg, response Data-> list of all the possible cases
                """
                status = None
                msg = None
                responseData = None
                try:  
                    data = request.json
                    exam_instance_id = data['exam_instance_id']
                    examCases =db.classroom_monitoring_db.session.query(db.exam_instance_cases).filter_by(exam_instance_id=exam_instance_id).all()
                    
                    # check for the validity of exam
                    if examCases is None:
                        status = 'failed'
                        msg = 'exam does not exist'
                        raise NotFound
                    responseData = {"cases": [] }
                    for i in examCases:
                                       
                        case_detailed_data = db.classroom_monitoring_db.session.query(db.frames).filter_by(case_id =i.case_id).first()
                        # case_detailed_data = db.classroom_monitoring_db.session.query(db.frames).filter(\
                        #    and_(db.frames.exam_instance_id==exam_instance_id,db.frames.student_number==i.student_number, \
                        #        db.frames.case_id == i.case_id)).first()
                        
                        
                        # if a case for any reason has a dropped frame we return it as null using this try catch block
                        try:
                            case_details = {'case_id': i.case_id, 'exam_instance_id': i.exam_instance_id, 
                            'stat':i.stat, 'confidence':str(i.confidence), 'ts': str(i.ts),  'student_number':i.student_number,    \
                                'case_image': case_detailed_data.image_link}
                            
                        except AttributeError as e:
                            case_details = {'case_id': i.case_id, 'exam_instance_id': i.exam_instance_id, 
                            'stat':i.stat, 'confidence':str(i.confidence), 'ts': str(i.ts),  'student_number':i.student_number,    \
                                'case_image': 'Not Found'}
                           
                            #case_detailed_data.image_link = None
                        responseData['cases'].append(case_details)
                    status = 'success'
                    msg = "Report generated successfully!"
                except KeyError:
                    status = 'failed'
                    msg = "Missing Parameter"  
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))

                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = "Error" 
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))             
                return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))

####################################################################################################
        @userNamespace.route('/get_recent_case/<string:exam_instance_id>')
        class get_recent_case(Resource):
            @api.doc(security='apikey')
            def get(self, exam_instance_id):
                """ -- API Description: This API is used to return the most recent case. this api is important
                since it is our way to check for the cases reported by the model and we get 
                the most recent case based on the timestamp
                --params: exam instance id
                --  return: status, msg, response data ->responseData = {"case_details": 'case_id' 'exam_instance_id'
                        'stat' 'confidence' 'timestamp'  'student_number'}]}                   
                
                """
                status = None
                msg = None
                responseData = None
                try:                 
                    # check for exam instance validity
                    exam = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                    if exam is None:
                        msg = 'Exam not found'
                        status = 'failed'
                        raise NotFound
                   # check if there is cases relate to this instance
                    examCases =db.classroom_monitoring_db.session.query(db.exam_instance_cases).filter(and_(db.exam_instance_cases.exam_instance_id== exam_instance_id,db.exam_instance_cases.stat !='C',db.exam_instance_cases.stat !="NC" ) ).order_by(db.exam_instance_cases.ts.desc()).first()
                    
                    if examCases is None:
                        responseData = None
                        msg = "No Recent Cases Detected"
                    else:
                        responseData = {"case_details": [{'case_id': examCases.case_id, 'exam_instance_id': examCases.exam_instance_id, 
                        'stat':examCases.stat, 'confidence':str(examCases.confidence), 'ts': str(examCases.ts), 'student_number':examCases.student_number}]}                   
                        msg = 'Recent Case Retreived successfully'
                    status = 'success'
                except KeyError:
                    msg = 'No Assigned Exam Instances found'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'No Assigned Exam Instances found'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
              
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
        ###########################################################################
        @userNamespace.route('/get_fps/<string:exam_instance_id>')
        class get_fps(Resource):
            @api.doc(security='apikey')
            def get(self, exam_instance_id):
                """ -- API Description: This API is used to return the fps assigned by the admin to a specific exam 
                -- params: exam instance id
                -- return: msg, status , data-> fps
                """
                status = None
                msg = None
                responseData = None
                try:
                    exam = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                    if exam is None:
                        msg = 'Exam not found'
                        status = 'failed'
                        raise NotFound
                    exam_instance_object = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id = exam_instance_id).first()
                    if exam_instance_object.fps is None :
                        msg = 'fps value is not found, or an error has occured'
                        status = 'failed'
                        raise NotFound  
                    responseData = exam_instance_object.fps
                    status = 'success'
                    msg = 'fps retrieved successfully'
                except KeyError:
                    msg = 'fps value is not found, or an error has occured'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'fps value is not found, or an error has occured'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
 ###############################################################################
        @userNamespace.route('/check_exam_ended/<string:exam_instance_id>')
        class get_fps(Resource):
            @api.doc(security='apikey')
            def get(self, exam_instance_id):
                """ 
                -- API Description: This API is used to check if the exam instance has finished
                -- params: exam instance id
                -- return : status, msg, data
                """
                status = None
                msg = None
                responseData = None
                try:
                    # check for exam
                    exam = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                    if exam is None:
                        msg = 'Exam not found'
                        status = 'failed'
                        raise NotFound
                    exam_instance_object = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id = exam_instance_id).first()
                    # check if exam ended or not yet
                    if exam_instance_object.ended == 0 :
                        msg = 'exam has NOT ended'
                        status = 'success'
                        responseData = json.loads(json.dumps('exam running'))
                    else:
                        msg = 'exam has ended'
                        status = 'success'
                        responseData = json.loads(json.dumps('exam ended'))

                        
                except KeyError:
                    msg = 'an error has occured'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'or an error has occured'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
 ###############################################################################
        @userNamespace.route('/end_exam/<string:exam_instance_id>')
        class get_fps(Resource):
            @api.doc(security='apikey')
            def get(self, exam_instance_id):
                """ 
                -- API Description: This API is used to end exam session
                -- params : exam_instance_id
                -- return: msg, status, data
                """
                
                status = None
                msg = None
                responseData = None
                try:
                    
                    # check if exam is found
                    exam = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                    if exam is None:
                        msg = 'Exam not found'
                        status = 'failed'
                        raise NotFound
                    exam_instance_object = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id = exam_instance_id).first()
                    # check if exam has already ended       
                    if exam_instance_object.ended == 1 :
                        msg = 'exam already ended'
                        status = 'success'
                        responseData = json.loads(json.dumps('exam already ended'))
                        raise NotFound

                    
                    # if the exam is running
                    
                    
                    db.classroom_monitoring_db.session.query(db.exam_instance).\
                    filter_by(exam_instance_id=exam_instance_id).\
                    update({'ended':1})
                    db.classroom_monitoring_db.session.commit()
                    msg = 'exam ended successfully'
                    status = 'success'
                    responseData = json.loads(json.dumps('exam ended successfully')) 
                except KeyError:
                    msg = 'an error has occured'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    msg = 'or an error has occured'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))