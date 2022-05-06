# imports all dependencies
from app import *
from __init__ import *
#######################
"""
Admin-level APIs
@description:
This file contains the implementation of all the Admin level APIs

All of our APIs return status, msg & data
status: success or failed
msg: representing the reason for failure or success
data(if any): data requested by the user 
"""    
#######################
class AdminLevelAPIs:
    @adminNamespace.route('/register_admin')
    class register_admin(Resource):    
        registerAdminPostData = api.model ("registerAdminData",{'national_id':fields.String(""),'password':fields.String(""),\
            'first_name':fields.String(""), 'last_name':fields.String(""),'job_role':fields.String("")})
        @api.doc(body=registerAdminPostData,security='apikey')
        def post(self):
            """ -- API Description: This API is used to register an admininstrator to the system 
                --params: national id, password, first name, last name, role
                --return data: status, msg, data
            """
            # return data of the request
            status =None
            msg = None 
            responseData =None

            #implementing a try Catch block to catch errors and report them
            try:
                #getting the request parameters
                data = request.json
                NationalID = data['national_id']
                password =data['password']
                FirstName =data['first_name']
                LastName=data['last_name']
                position= data['job_role']
                msg = 'Administrator Added Successfully!'
                status = 'success'     
                
                # check if password is follows certain rules:
                # minimum eight characters, at least one letter, one number and one special character
                if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",password):
                    msg = "password needs to include Minimum eight characters, at least one letter, one number and one special character"
                    status = 'failed'
                    raise NotFound
                
                # using salting technique in storing passwords in the database
                # by concatinating the password with the app secret key
                # then hash it using md5
                salt = password + app.config['SECRET_KEY']
                db_pass = hashlib.md5(salt.encode()).hexdigest()
                
                # add new admin in the database
                newAdmin = db.admin(national_id = NationalID, passwd= db_pass, first_name=FirstName,\
                    last_name=LastName, job_role=position)
                db.classroom_monitoring_db.session.add(newAdmin)
                db.classroom_monitoring_db.session.commit()

            # error in the parameters
            except KeyError:
                msg = 'Missing Parameter'
                status = 'failed'
                return json.loads(json.dumps({'status': status, 'msg':msg, 'data': responseData}))
            except NotFound:
                return json.loads(json.dumps({'status': status, 'msg': msg, 'data': responseData}))
            
            # we use that exception to indicate errors such as adding user with the same primary key
            except sqlalchemy.exc.IntegrityError as e:
                msg  ="User Already Exists"
                return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
            except:
                db.classroom_monitoring_db.session.rollback()
                raise
            finally:
                db.classroom_monitoring_db.session.close()                

            return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
    #########################################################################
        @adminNamespace.route('/login_admin')
        class login_admin(Resource): 
            
            loginAdminData = api.model ("loginAdminData",{'national_id':fields.String(""),\
                'password':fields.String("")})
            @api.doc(body = loginAdminData,security='apikey')
            def post(self):            
                """ -- API Description: This API is used to login an admininstrator to the system 
                    --params: national id, password
                    --return data: status, msg, data
                """
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json
                    NationalID = data['national_id']
                    password = data['password']
                    
                    # we first hash the entered password by the user
                    salt = password + app.config['SECRET_KEY']
                    db_pass = hashlib.md5(salt.encode()).hexdigest()
                    # we check if there is a user with matching the entered data
                    user =db.classroom_monitoring_db.session.query(db.admin).filter_by(national_id=NationalID).first()
                    # the user not found
                    if user is None:
                        status= 'failed'
                        msg = 'User Not Found'     
                        raise NotFound
                    #user found but password is incorrect
                    if db_pass != user.passwd:
                        status= 'failed'
                        msg = 'incorrect username or password'                   
                        raise NotFound
                    status= 'Success'
                    msg = 'Admin logged in successfully!'
                # error in the parameters                    
                except KeyError:
                    status= 'failed'
                    msg = 'Missing Parameter'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                # we use that exception to indicate errors such as adding user with the same primary key
                except sqlalchemy.exc.IntegrityError as e:
                    status= 'failed'
                    msg = 'User Already Exists'                   
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
#############################################################################################################
        @adminNamespace.route('/create_exam_instance')
        class create_exam_instance(Resource):
            examInstanceData = api.model ("examInstanceData",{'exam_instance_id':fields.String(""),\
                'exam_reference_code':fields.String(""),\
                    'school_name':fields.String(""), 'admin_national_id':fields.String(""),\
                        'camera_static_ip':fields.String(""), 'fps':fields.Integer()})
            @api.doc(body = examInstanceData,security='apikey')
            def post(self):               
                """
                -- API Description: This API is used to Create Exam Instance and by default 
                --params: exam instance id, exam reference code , school name , admin national id, camera static ip                
                --return data: status, msg, data
                """
                status = None
                msg = None
                responseData = None
                try:
                    data = request.json
                    examInstanceID = data['exam_instance_id']
                    examRefCode = data['exam_reference_code']
                    SchoolName = data['school_name']
                    adminNatID = data['admin_national_id']
                    camera_static_ip = data['camera_static_ip']
                
                    # admin not found
                    user =db.classroom_monitoring_db.session.query(db.admin).filter_by(national_id=adminNatID).first()
                    if user is None:
                        status = 'failed'
                        msg = 'admin not found'
                        raise NotFound
                    
                    # else admin is found
                    # add to data base
                    newRoom = db.exam_instance(exam_instance_id = examInstanceID, exam_reference_code= examRefCode, school_name=SchoolName,\
                        admin_national_id = adminNatID, camera_static_ip= camera_static_ip)
                    db.classroom_monitoring_db.session.add(newRoom)
                    db.classroom_monitoring_db.session.commit()
                
                    msg = "exam instance created Successfully!"
                    status ='Success'
               # error in the parameters
                except KeyError:
                    status = 'failed'
                    msg = 'Missing Parameter'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))           
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = 'exam instance Already Exists'
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))

                return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                
    # ##############################################################    
        @adminNamespace.route('/assign_proctor_to_exam')
        class assign_proctor_to_exam(Resource):
            proctorExamAssignmentData = api.model ("proctorExamAssignmentData",{'admin_national_id':fields.String(""),\
                'proctor_national_id':fields.String(""),'exam_instance_id':fields.String("")})
            @api.doc(body = proctorExamAssignmentData,security='apikey')
            def post(self):
                """ 
                -- API Description: This API is used to by the admin to assign a proctor to exam instance 
                --params: admin national id, proctor national  id, exam instance id c
                --return data: status, msg, data
                """
                status = None
                msg = None
                responseData = None

                try:   
                    data = request.json
                    adminNatID = data['admin_national_id']
                    proctorNatID = data['proctor_national_id']
                    examInstanceID = data['exam_instance_id']
                    
                    '''checks for the entered data'''
                    # admin not found
                    a =db.classroom_monitoring_db.session.query(db.admin).filter_by(national_id=adminNatID).first()
                    if a is None:
                        raise NotFound
                    
                    # proctor not found
                    p =db.classroom_monitoring_db.session.query(db.proctor).filter_by(national_id=proctorNatID).first()
                    if p is None:
                        status = 'failed'
                        msg = "Admin Not Found"
                        raise NotFound
                    
                    # exam not found
                    eid =db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=examInstanceID).first()
                    if eid is None:
                        status = 'failed'
                        msg = "Exam Instance Not Found"
                        raise NotFound
                    
                    # else data is correct
                    newAssignment = db.admin_assign_proctor(admin_national_id = adminNatID, proctor_national_id= proctorNatID, \
                        exam_instance_id = examInstanceID)
                    
                    new_proctor_exam = db.proctor_monitor_exam(proctor_national_id= proctorNatID, \
                        exam_instance_id = examInstanceID)
                    db.classroom_monitoring_db.session.add(newAssignment)
                    db.classroom_monitoring_db.session.commit()
                    db.classroom_monitoring_db.session.add(new_proctor_exam)
                    db.classroom_monitoring_db.session.commit()
                
                    status = 'success'
                    msg = "Assignment Completed Successfully!"
                
                except KeyError:
                    status = 'failed'
                    msg = "Admin or Proctor or Exam Instance ID Not Found"
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except NotFound:
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                except sqlalchemy.exc.IntegrityError as e:
                    status = 'failed'
                    msg = "Assignment Already Exists"
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
        
    # ###############################################################
        @adminNamespace.route('/register_proctor')
        class register_proctor(Resource):
                registerProctorData = api.model ("registerProctorData",{'national_id':fields.String(""),'password':fields.String(""),\
                    'first_name':fields.String(""), 'last_name':fields.String(""),\
                        'school_name':fields.String("")})
                @api.doc(body=registerProctorData,security='apikey')
                def post(self):
                    """ 
                    -- API Description: This API is used to register an invigilator to the system
                    --params: national id, password, first name, last name, school_name
                    --return data: status, msg, data
                    
                    """
                    status = None
                    msg = None
                    responseData = None

                    try:  
                        data = request.json
                        NationalID = data['national_id']
                        password = data['password']
                        FirstName = data['first_name']
                        LastName = data['last_name']
                        SchoolName = data['school_name']
                        
                        # check that password meets our requirements
                        # min 8 chars, at least one letter, one number and one special character
                        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",password):
                            status = 'failed'
                            msg = "Password needs to include Minimum eight characters, at least one letter, one number and one special character"
                            raise NotFound
                        salt = password + app.config['SECRET_KEY']
                        db_pass = hashlib.md5(salt.encode()).hexdigest()
                        new_proctor = db.proctor(national_id = NationalID, passwd= db_pass, first_name=FirstName,\
                            last_name=LastName, school_name=SchoolName)
                        db.classroom_monitoring_db.session.add(new_proctor)
                        db.classroom_monitoring_db.session.commit()
                    
                        status = 'success'
                        msg = "Proctor Added Successfully!"
                    except KeyError:
                        status = 'failed'
                        msg = "Missing Parameter"  
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                    except NotFound:
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                
                    except sqlalchemy.exc.IntegrityError as e:
                        status = 'failed'
                        msg = "User Already Exists" 
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
               
                    ###############################################################
                    
        @adminNamespace.route('/add_students_to_exam')
        class add_students_to_exam (Resource):
                addStudentsData = api.model ("addStudentsData",{'exam_instance_id': fields.String("")})
                @api.doc(body=addStudentsData,security='apikey')
                def post(self):
                    """ 
                    -- API Description: This API is used to add students to specific exam instance, by default it adds
                    15 students to an exam, but there is room to increase capacity.
                    for now we assume that the student number is the student ID. But in future versions, we will include the student id as well.
                    
                    @parameter: exam instance id
                    @return value: status, msg, resonse data                    
                    """
                    status = None
                    msg = None
                    responseData = None

                    try:  
                        data = request.json
                        exam_instance_id = data['exam_instance_id']
                        eid =db.classroom_monitoring_db.session.query(db.exam_instance).filter_by(exam_instance_id=exam_instance_id).first()
                        # check if the exam instance entered exists
                        if eid is None:
                            status = 'failed'
                            msg = 'Exam Doesnot exist'                            
                            raise NotFound
                        
                        for i in range (1,16): 
                            students_to_exam = db.students_positions(student_number = i,exam_instance_id = exam_instance_id)
                            db.classroom_monitoring_db.session.add(students_to_exam)
                        db.classroom_monitoring_db.session.commit()
                        status = 'success'
                        msg = "Students Added Successfully!"
                    except KeyError:
                        status = 'failed'
                        msg = "Missing Parameter"  
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
                    except NotFound:
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))                
                    except sqlalchemy.exc.IntegrityError as e:
                        status = 'failed'
                        msg = "Student Already Exists" 
                        return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))             
                    return json.loads(json.dumps({'status': status, 'msg': msg,'data': responseData}))
