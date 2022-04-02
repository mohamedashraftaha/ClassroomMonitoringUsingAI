# imports all dependencies
from imports.imports import *
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
                except KeyError:
                    json.dumps({'status': 'Success', 'message': "exam instance created Successfully!"})

                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "User Not Found"})
                except sqlalchemy.exc.IntegrityError as e:
                    return json.dumps({'status': 'fail', 'message': "User Already Exists"})

                return json.dumps({'status': 'Success', 'message': "Proctor logged in successfully!"})
# ######################################################################
        @userNamespace.route('/create_possible_case')
        class create_possible_case(Resource):
            CreateIncidentData = api.model ("CreateIncidentData",{'exam_instance_id':fields.String(""),\
                'stat':fields.String("")})
            @api.doc(body=CreateIncidentData)
            def post(self):
                """ @API Description: This API is used to CreateIncident """                        
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
                except KeyError:
                    json.dumps({'status': 'Success', 'message': "exam instance created Successfully!"})
                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "Invalid!"})
                except sqlalchemy.exc.IntegrityError as e:
                    print(e.args)
                    return json.dumps({'status': 'fail', 'message': "Incident Already Exists or not found"})

                return json.dumps({'status': 'Success', 'message': "Incident Completed Successfully!"})
#######################################
        @userNamespace.route('/dismiss_case')
        class dismiss_case(Resource):
            dismissData = api.model ("dismissData",{'caseID':fields.String("")})
            @api.doc(body=dismissData)
            def post(self):
                """ @API Description: This API is used to update status to Not cheating """
                try:
                    data = request.json        
                    caseID = data['caseID']
                    db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter_by(case_id=caseID).\
                    update({'stat':'NC'})
                    db.classroom_monitoring_db.session.commit()
                except KeyError:
                    return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
            
                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "Invalid!"})
                except sqlalchemy.exc.IntegrityError as e:
                    print(e.args)
                    return json.dumps({'status': 'fail', 'message': "Incident Already marked or not found"})

                return json.dumps({'status': 'Success', 'message': "Incident Completed Successfully!"})
##########################################################
        @userNamespace.route('/report_case')
        class report_case(Resource):
            reportData = api.model ("reportData",{'caseID':fields.String("")})
            @api.doc(body=reportData)
            def post(self):
                """ @API Description: This API is used to update status to  cheating """
    
                #getting the request parameters
                try:
                    data = request.json            
                    caseID = data['caseID']
                    
                    db.classroom_monitoring_db.session.query(db.exam_instance_cases).\
                    filter_by(case_id=caseID).\
                    update({'stat':'C'})
                    db.classroom_monitoring_db.session.commit()
                except KeyError:
                    return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})

                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "Invalid!"})
                except sqlalchemy.exc.IntegrityError as e:
                    print(e.args)
                    return json.dumps({'status': 'fail', 'message': "Incident Already marked or not found"})

                return json.dumps({'status': 'Success', 'message': "Incident Completed Successfully!"})
################################################################

        @userNamespace.route('/get_frames_links/<int:caseID>')
        class get_frames_links(Resource):
            @cross_origin()
            def get(self, caseID):
                """ @API Description: This API is used to retrieve links of the frames of a given cheating incident """
                urlList  = []
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
                    return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})
              
                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "Invalid!"})
                except sqlalchemy.exc.IntegrityError as e:
                    print(e.args)
                    return json.dumps({'status': 'fail', 'message': "Frames Already exsist"})

                return json.dumps({'status': 'Success', 'message': "Incident Completed Successfully!", 'urls': urlList})
