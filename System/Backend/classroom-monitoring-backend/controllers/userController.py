# imports all dependencies
from imports.imports import *
from app import *
#######################
"""User-level APIs"""    
#######################
class UserLevelAPIs:
    @userlNameSpace.route('/user/registerProctor')
    class registerProctor(Resource):
        registerProctorData = api.model ("registerProctorData",{'national_id':fields.String("1"),'password':fields.String("$Test123"),'first_name':fields.String("Mohamed"), 'last_name':fields.String("Ashraf"),'school_name':fields.String("AUC")})
        @api.doc(body=registerProctorData)
        def post(self):
            """ @API Description: This API is used to register an invigilator to the system """
            try:  
                data = request.json
                NationalID = data['national_id']
                password = data['password']
                FirstName = data['first_name']
                LastName = data['last_name']
                SchoolName = data['school_name']
                if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",password):
                    msg = "Password needs to include Minimum eight characters, at least one letter, one number and one special character"
                    raise NotFound
                salt = password + app.config['SECRET_KEY']
                db_pass = hashlib.md5(salt.encode()).hexdigest()
                new_proctor = db.proctor(NationalID = NationalID, passwd= db_pass, FirstName=FirstName,\
                    LastName=LastName, SchoolName=SchoolName)
                db.classroom_monitoring_db.session.add(new_proctor)
                db.classroom_monitoring_db.session.commit()
            except KeyError:
                json.dumps({'status': 'Success', 'message': "exam instance created Successfully!"})
          
            except sqlalchemy.exc.IntegrityError as e:
                return json.dumps({'status': 'fail', 'message': "User Already Exists"})

            return json.dumps({'status': 'Success', 'message': "Proctor Added Successfully!"})

        
        @userlNameSpace.route('/user/loginProctor')
        class loginProctor(Resource):
            LoginProctorData = api.model ("LoginProctorData",{'national_id':fields.String("1"),'password':fields.String("$Test123")})
            @api.doc(body=LoginProctorData)
            def post(self):
                """ @API Description: This API is used to login an Proctor to the system """            
                try:   
                    data = request.json
                    NationalID = data['national_id']
                    password = data['password']
                    salt = password + app.config['SECRET_KEY']
                    db_pass = hashlib.md5(salt.encode()).hexdigest()
                    user =db.session.query(db.proctor).filter_by(NationalID=NationalID).first()
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
        @userlNameSpace.route('/user/CreateIncident')
        class CreateIncident(Resource):
            CreateIncidentData = api.model ("LoginProctorData",{'examroom_id':fields.String("1"),'stat':fields.String("$Test123")})
            @api.doc(body=CreateIncidentData)
            def post(self):
                """ @API Description: This API is used to CreateIncident """                        
                try:   
                    data = request.json
                    ExamRoomID = data['examroom_id']
                    state = data['stat']                
                    erid = db.session.query(db.ExamRoom).filter_by(ExamroomID= ExamRoomID)
                    if erid is None:
                            raise NotFound
                    newincident=db.examincidents(stat=state, ExamroomID= ExamRoomID)
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
        @userlNameSpace.route('/user/dismiss')
        class dismiss(Resource):
            dismissData = api.model ("dismissData",{'IncidentID':fields.String("1")})
            @api.doc(body=dismissData)
            def post(self):
                """ @API Description: This API is used to update status to Not cheating """
                try:
                    data = request.json        
                    Incident = data['IncidentID']
                    db.session.query(db.examincidents).\
                    filter_by(IncidentID=Incident).\
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
        @userlNameSpace.route('/user/report')
        class report(Resource):
            reportData = api.model ("reportData",{'IncidentID':fields.String("1")})
            @api.doc(body=reportData)
            def post(self):
                """ @API Description: This API is used to update status to  cheating """
    
                #getting the request parameters
                try:
                    data = request.json            
                    Incident = data['IncidentID']
                    
                    db.session.query(db.examincidents).\
                    filter_by(IncidentID=Incident).\
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

        @userlNameSpace.route('/user/getFramesLinks')
        class report(Resource):
            getFramesLinksData = api.model ("getFramesLinksData",{'IncidentID':fields.String("1")})
            @api.doc(body=getFramesLinksData)
            @cross_origin()
            def get(self):
                """ @API Description: This API is used to retrieve links of the frames of a given cheating incident """
    
                response = None
                #getting the request parameters
                IncidentID = request.args.get("incidentID")
                urlList  = []
                try:
                    IncidentID = request.args.get("incidentID")
                    
                    client=boto3.client('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key,config=Config(region_name = 'eu-north-1'   ,signature_version='s3v4'))
                    session = boto3.Session(
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_access_key,
                    )
                    bucket='classroommonitoring'
                    temp= IncidentID #to change between images
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
                                erid = db.session.query(db.frames).filter_by(incidentID= IncidentID)
                                if erid is None:
                                    raise NotFound   
                                print(url)
                                urlList.append(url)
                                print('success{}'.format(i+1))
                                newframe=db.frames(imageLink=url, incidentID= IncidentID)
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
