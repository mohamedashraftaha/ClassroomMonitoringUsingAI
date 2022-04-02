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
                        raise NotFound
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
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg= "User Already Exists"
                    return json.loads(json.dumps({'status': status, 'msg':msg, 'data': responseData}))
                
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
# ######################################################################
        @userNamespace.route('/create_possible_case')
        class create_possible_case(Resource):
            CreateIncidentData = api.model ("CreateIncidentData",{'exam_instance_id':fields.String(""),\
                'stat':fields.String("")})
            @api.doc(body=CreateIncidentData)
            def post(self):
                """ @API Description: This API is used to CreateIncident """                        
                status = None
                msg = None
                responseData = None
                try:   
                    data = request.json
                    examInstanceID = data['exam_instance_id']
                    state = data['stat']                
                    erid = db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id= examInstanceID)
                    if erid is None:
                            raise NotFound
                    newincident=db.exam_instance_cases(stat=state, exam_instance_id= examInstanceID)
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
                    msg = 'Invalid!'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'Incident Already Exists or not found'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
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
                    msg = 'Invalid'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'Process of dismissing the case failed!'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
            
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
##########################################################
        @userNamespace.route('/report_case')
        class report_case(Resource):
            reportData = api.model ("reportData",{'caseID':fields.String("")})
            @api.doc(body=reportData)
            def post(self):
                """ @API Description: This API is used to update status to  cheating """
    
                #getting the request parameters
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json            
                    caseID = data['caseID']
                    
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
                    msg = 'Invalid'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
       
                    status = 'failed'
                    msg = 'Process of reporting the case failed!'
                    print(e.args)
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))

                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
################################################################

        @userNamespace.route('/get_frames_links/<string:caseID>')
        class get_frames_links(Resource):
            @cross_origin()
            def get(self, caseID):
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
                    for i in mybucket.objects.all():
                        if str(i.key) == str('c{}-{}.jpg'.format(temp,j+1)):
                            j+=1
                    for i in range(j):
                        try: 
                        # client.download_file(bucket, 'c{}-{}.jpg'.format(temp,i), './c{}-{}.jpg'.format(temp,i))
                                url = client.generate_presigned_url('get_object',Params={ 'Bucket': bucket, 'Key': 'c{}-{}.jpg'.format(temp,i+1) }, HttpMethod="GET",ExpiresIn=9800)   
                                erid = db.classroom_monitoring_db.session.query(db.frames).filter_by(case_id= caseID)
                                if erid is None:
                                    raise NotFound   
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
                    msg = 'Invalid!'
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'Frames Already exists'
       
                    print(e.args)
                    return json.loads(json.dumps({'status': status, 'msg': msg, 'data': urlList}))
 
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
                        msg = 'No Assigned Exam Instances to this user'
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
                
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))