# imports all dependencies
from app import *
from . import *
#######################
"""User-level APIs"""    
#######################
class UserLevelAPIs:

        @userNamespace.route('/login_proctor')
        class login_proctor(Resource):
            
            LoginProctorData = api.model ("LoginProctorData",{'national_id':fields.String(""),\
                'password':fields.String("")})
            @api.doc(body=LoginProctorData)
            def post(self):
                """ @API Description: This API is used to login an Proctor to the system """            
                
                status = None
                msg = None
                responseData = None
                try:   
                    data = request.json
                    NationalID = data['national_id']
                    password = data['password']
                    salt = password + app.config['SECRET_KEY']
                    db_pass = hashlib.md5(salt.encode()).hexdigest()
                    user =db.classroom_monitoring_db.session.query(db.proctor).filter_by(national_id=NationalID).first()
                    if user is None:
                        raise NotFound
                    if db_pass != user.passwd:
                        raise IncorrectData

                    status = 'success'
                    msg = "Proctor logged in successfully!"
                except KeyError:
                    status = 'failed'
                    msg= 'Missing Parameter'
                    json.loads(json.dumps({'status': status, 'msg': msg, 'data':responseData}))

                except NotFound:
                    status = 'failed'
                    msg= "User Not Found"
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data':responseData}))
                except IncorrectData:
                    status = 'failed'
                    msg = "Password needs to include Minimum eight characters, at least one letter, one number and one special character"
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                

                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg= "User Already Exists"
                    return json.loads(json.dumps({'status': status, 'msg':msg, 'data': responseData}))
              
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
# ######################################################################
        @userNamespace.route('/create_possible_case')
        class create_possible_case(Resource):
            CreateIncidentData = api.model ("CreateIncidentData",{'case_id':fields.Integer(),'exam_instance_id':fields.String(""),\
                'stat':fields.String(""), 'confidence': fields.Float()})
            @api.doc(body=CreateIncidentData)
            def post(self):
                """ @API Description: This API is used to CreateIncident """                        
                status = None
                msg = None
                responseData = None
                try:   
                    data = request.json
                    case_id = data['case_id']
                    examInstanceID = data['exam_instance_id']
                    state = data['stat']      
                    confidence = data['confidence']          
                    erid = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id= examInstanceID)
                    if erid is None:
                            raise NotFound
                    newincident=db.exam_instance_cases(case_id=case_id,stat=state, exam_instance_id= examInstanceID, confidence = confidence)
                    db.classroom_monitoring_db.session.add(newincident)
                    db.classroom_monitoring_db.session.commit()
                    status = 'success'
                    msg = 'Incident Completed Successfully!'
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except NotFound:
                    status = 'failed'
                    msg = 'Exam Incident Doesnot exist'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
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
            dismissData = api.model ("dismissData",{'caseID':fields.String("")})
            @api.doc(body=dismissData)
            def post(self):
                """ @API Description: This API is used to update status to Not cheating """
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json        
                    caseID = data['caseID']
                    
                    dbcases = db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter_by(case_id=caseID).first()
                    
                    if dbcases is None:
                        raise NotFound

                    db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter_by(case_id=caseID).\
                    update({'stat':'NC'})
                    db.classroom_monitoring_db.session.commit()                   
                    status = 'success'
                    msg = 'Case Dismissed Successfully'
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except NotFound:
                    status = 'failed'
                    msg = 'Case ID not found'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'Process of dismissing the case failed!'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
          
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
##########################################################
        @userNamespace.route('/report_case')
        class report_case(Resource):
            reportCaseData = api.model ("reportCaseData",{'caseID':fields.String("")})
            @api.doc(body=reportCaseData)
            def post(self):
                """ @API Description: This API is used to update status to  cheating """
    
                #getting the request parameters
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json            
                    caseID = data['caseID']                    
                    
                    dbcases = db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter_by(case_id=caseID).first()
                    
                    if dbcases is None:
                        raise NotFound
                    
                    db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter_by(case_id=caseID).\
                    update({'stat':'C'})
                    db.classroom_monitoring_db.session.commit()
                    status = 'success'
                    msg = 'Case Reported Successfully'
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'       
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except NotFound:
                    status = 'failed'
                    msg = 'Case ID not found'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:     
                    status = 'failed'
                    msg = 'Process of reporting the case failed!'
                    print(e.args)
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except:
                    db.classroom_monitoring_db.session.rollback()
                    raise
                finally:
                     db.classroom_monitoring_db.session.close()
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
################################################################

        @userNamespace.route('/get_frames_links/<int:caseID>/<string:exam_instance_id>')
        class get_frames_links(Resource):
            @cross_origin()
            def get(self, caseID, exam_instance_id):
                """ @API Description: This API is used to retrieve links of the frames of a given cheating incident """
                urlList  = []
                status = None
                msg = None                
                try:
                    client=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,config=Config(region_name = 'eu-north-1'   ,signature_version='s3v4'))
                    session = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_access_key,
                    )
                    bucket='classroommonitoring'
                    temp= caseID #to change between images
                    j=0
                    s3 = session.resource('s3')
                    mybucket=s3.Bucket(bucket)
                    status = 'success'
                    msg = 'frames retrieved successfully'
                    checker = db.classroom_monitoring_db.session.query(db.exam_instance_cases).filter(and_(db.exam_instance_cases.case_id== caseID, db.exam_instance_cases.exam_instance_id == exam_instance_id)).first()
                    if checker is None:
                        raise NotFound 
 
                           
                    for i in mybucket.objects.all():
                        if str(i.key) == str('c{}-{}-{}.jpg'.format(temp,exam_instance_id,j+1)):
                            j+=1
                    for i in range(j):
                        try: 
                        # client.download_file(bucket, 'c{}-{}.jpg'.format(temp,i), './c{}-{}.jpg'.format(temp,i))
                                url = client.generate_presigned_url('get_object',Params={ 'Bucket': bucket, 'Key': 'c{}-{}.jpg'.format(temp,i+1) }, HttpMethod="GET",ExpiresIn=9800)   
                                print(url)
                                urlList.append(url)
                                print('success{}'.format(i+1))
                                newframe=db.frames(image_link=url, case_id= caseID)
                                db.classroom_monitoring_db.session.add(newframe)
                                db.classroom_monitoring_db.session.commit()
    
                        except sqlalchemy.exc.IntegrityError as e:
                            print(e.args)
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'  
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))              
                except NotFound:
                    status = 'failed'
                    msg = 'Case/Exam ID does not Exist'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
                except sqlalchemy.exc.IntegrityError as e:
                    print("HERE2")
                    status = 'failed'
                    msg = 'frames already exists'       
                    print(e.args)
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
                except sqlalchemy.exc.PendingRollbackError as e:     
                    print("HERE2")
                    status = 'failed'
                    msg = 'Case ID Does Not exist'      
                    urlList  = None
                    db.classroom_monitoring_db.session.rollback()
                    print(e.args)
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
            @cross_origin()
            def get(self,proctor_national_id):
                """ @API Description: This API is used to retrieve all exam instances assigned to the proctor, if any """
                status = None
                msg = None
                responseData = None
                try:
                    # search for the assigned exam instances
                    assigned_instances = db.classroom_monitoring_db.session.query(db.admin_assign_proctor).\
                        filter_by(proctor_national_id = proctor_national_id).first()
                    if assigned_instances is None:
                        raise NotFound   
                    responseData = assigned_instances.exam_instance_id
                    msg = 'Exam Instance ID Retrieved Successfully'
                    status = 'success'
                except KeyError:
                    msg = 'No Assigned Exam Instances to this user'
                    status = 'failed'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    msg = 'No Assigned Exam Instances to this user'
                    status = 'failed'
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
            @api.doc(body=model_sensitivity)
            def post(self):
                """ @API Description: This API is used to adjust the model sensitivity """
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
                        msg = 'Exam Instance ID'
                        status = 'failed'
                        raise NotFound   
                    if exam_instance.exam_instance_id != exam_instance_id:
                        msg = 'No Assigned Exam Instances to this user'
                        status = 'failed'        
                        raise IncorrectData                   
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
                except IncorrectData:
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
            def get(self, examInstanceID):
                """ @API Description: This API is used to return all details of an exam instance """
                status = None
                msg = None
                responseData = None
                try:                  
                    exam_instance_details = db.classroom_monitoring_db.session.query(db.exam_instance).\
                        filter_by(exam_instance_id = examInstanceID).first()    
                    if exam_instance_details is None:
                        msg = 'No details for the selected exam instance'
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
                @api.doc(body=addStudentsLocations)
                def post(self):
                    """ @API Description: This API is used to add students locations based on the bounding boxes generated by YOLO"""
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
                        if eid is None:
                            raise NotFound
                        if snum is None:
                             raise IncorrectData
                         
                         
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
                        status = 'failed'
                        msg = 'Exam Doesnot exist'
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                
                    except IncorrectData:
                        status = 'failed'
                        msg = 'Student Does not exist'
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
            @api.doc(body=reportData)
            def post(self):
                """ @API Description: This API is used to generate end of exam report of ALL cases either reported or dismissed"""
                status = None
                msg = None
                responseData = None
                try:  
                    data = request.json
                    exam_instance_id = data['exam_instance_id']
                    
                    examCases =db.classroom_monitoring_db.session.query(db.exam_instance_cases).filter_by(exam_instance_id=exam_instance_id).all()
                    if examCases is None:
                        raise NotFound
                    responseData = {"cases": [] }
                    for i in examCases:
                        case_details = {"case_details": [{'case_id': i.case_id, 'exam_instance_id': i.exam_instance_id, 
                        'stat':i.stat, 'confidence':str(i.confidence), 'ts': str(i.ts)}]}
                        responseData['cases'].append(case_details)
                    status = 'success'
                    msg = "Report generated successfully!"
                except KeyError:
                    status = 'failed'
                    msg = "Missing Parameter"  
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))

                except NotFound:
                    status = 'failed'
                    msg = 'Exam Does not exist'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                
                
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = "Error" 
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))             
                return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))

####################################################################################################
        @userNamespace.route('/get_recent_case/<string:exam_instance_id>')
        class get_recent_case(Resource):
            def get(self, exam_instance_id):
                """ @API Description: This API is used to return the most recent case """
                status = None
                msg = None
                responseData = None
                try:                 
                    
                    exam = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                    if exam is None:
                        msg = 'Exam not found'
                        status = 'failed'
                        raise NotFound
                    examCases =db.classroom_monitoring_db.session.query(db.exam_instance_cases).filter(and_(db.exam_instance_cases.exam_instance_id== exam_instance_id,db.exam_instance_cases.stat !='C',db.exam_instance_cases.stat !="NC" ) ).order_by(db.exam_instance_cases.ts.desc()).first()
                    
                    if examCases is None:
                        responseData = None
                        msg = "No Recent Cases Detected"
                    else:
                        responseData = {"case_details": [{'case_id': examCases.case_id, 'exam_instance_id': examCases.exam_instance_id, 
                        'stat':examCases.stat, 'confidence':str(examCases.confidence), 'ts': str(examCases.ts)}]}                   
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
          