# imports all dependencies
from imports.imports import *
from app import *
#######################
"""Admin-level APIs"""    
#######################
class AdminLevelAPIs:
    @adminNamespace.route('/admin/registerAdmin')
    class registerAdmin(Resource):    
        registerAdminPostData = api.model ("registerAdminData",{'national_id':fields.String("1"),'password':fields.String("$Test123"),'first_name':fields.String("Mohamed"), 'last_name':fields.String("Ashraf"),'position':fields.String("Teacher")})
        @api.doc(body=registerAdminPostData)
        def post(self):
            """ @API Description: This API is used to register an admininstrator to the system """
            #getting the request parameters
            try:
                data = request.json
                NationalID = data['national_id']
                password = data['password']
                FirstName = data['first_name']
                LastName = data['last_name']
                position = data['position']
            except KeyError:
                    return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})        
            try:
                if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",password):
                    msg = "Password needs to include Minimum eight characters, at least one letter, one number and one special character"
                    raise NotFound
                salt = password + app.config['SECRET_KEY']
                db_pass = hashlib.md5(salt.encode()).hexdigest()
                newAdmin = db.Admin(NationalID = NationalID, passwd= db_pass, FirstName=FirstName,\
                    LastName=LastName, position=position)
                db.classroom_monitoring_db.session.add(newAdmin)
                db.classroom_monitoring_db.session.commit()
            except NotFound:
                return json.dumps({'status': 'fail', 'message': msg})
            except sqlalchemy.exc.IntegrityError as e:
                return json.dumps({'status': 'fail', 'message': "User Already Exists"})

            return json.dumps({'status': 'Success', 'message': "Administrator Added Successfully!"})
    #########################################################################
        @adminNamespace.route('/admin/loginAdmin')
        class loginAdmin(Resource): 
 
            loginAdminData = api.model ("loginAdminData",{'national_id':fields.String("1"),'password':fields.String("$Test123")})
            @api.doc(body = loginAdminData)
            def post(self):            
                """ @API Description: This API is used to login an admininstrator to the system """

                try:
                    data = request.json
                    NationalID = data['national_id']
                    password = data['password']
                    salt = password + app.config['SECRET_KEY']
                    db_pass = hashlib.md5(salt.encode()).hexdigest()
                    user =db.classroom_monitoring_db.session.query(db.Admin).filter_by(NationalID=NationalID).first()
                    if user is None:
                        raise NotFound
                    if db_pass != user.passwd:
                        raise NotFound
                except KeyError:
                        return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})        
                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "User Not Found"})
                except sqlalchemy.exc.IntegrityError as e:
                    return json.dumps({'status': 'fail', 'message': "User Already Exists"})

                return json.dumps({'status': 'Success', 'message': "Admin logged in successfully!"})
#############################################################################################################
        @adminNamespace.route('/admin/createExamInstance')
        class createExamInstance(Resource):
            examInstanceData = api.model ("examInstanceData",{'examroom_id':fields.String("1"),'exam_id':fields.String("$Test123"),'school_name':fields.String("Mohamed"), 'admin_national_id':fields.String("Ashraf")})
            @api.doc(body = examInstanceData)
            def post(self):               
                """ @API Description: This API is used to Create Exam Instance """
                try:
                    data = request.json
                    ExamRoomID = data['examroom_id']
                    ExamID = data['exam_id']
                    SchoolName = data['school_name']
                    adminNatID = data['admin_national_id']
                
                    # admin not found
                    user =db.classroom_monitoring_db.session.query(db.Admin).filter_by(NationalID=adminNatID).first()
                    if user is None:
                        raise NotFound
                    
                    # else admin is found
                    newRoom = db.ExamRoom(ExamroomID = ExamRoomID, ExamID= ExamID, SchoolName=SchoolName,\
                        admin_national_id = adminNatID)
                    db.classroom_monitoring_db.session.add(newRoom)
                    db.classroom_monitoring_db.session.commit()
                except KeyError:
                        return json.dumps({'status': 'fail', 'message': 'Missing Parameter'})          
                
                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "Admin Not Found"})
                except sqlalchemy.exc.IntegrityError as e:
                    return json.dumps({'status': 'fail', 'message': "exam instance Already Exists"})

                return json.dumps({'status': 'Success', 'message': "exam instance created Successfully!"})
                
    # ##############################################################    
        @adminNamespace.route('/admin/proctorExamAssignment')
        class proctorExamAssignment(Resource):
            proctorExamAssignmentData = api.model ("proctorExamAssignmentData",{'admin_national_id':fields.String("1"),'proctor_national_id':fields.String("$Test123"),'exam_room_id':fields.String("Mohamed")})
            @api.doc(body = proctorExamAssignmentData)
            def post(self):
                """ @API Description: This API is used to by the admin to assign a proctor to exam instance """
                try:   
                    data = request.json
                    adminNatID = data['admin_national_id']
                    proctorNatID = data['proctor_national_id']
                    AssignedExamRoomID = data['exam_room_id']
                    
                    # admin not found
                    a =db.session.query(db.Admin).filter_by(NationalID=adminNatID).first()
                    if a is None:
                        raise NotFound
                    
                    # admin not found
                    p =db.session.query(db.proctor).filter_by(NationalID=proctorNatID).first()
                    if p is None:
                        raise NotFound
                    
                    # admin not found
                    eid =db.session.query(db.ExamRoom).filter_by(ExamroomID=AssignedExamRoomID).first()
                    if eid is None:
                        raise NotFound
                    
                    # else admin is found
                    newAssignment = db.proctorExamAssignment(admin_national_id = adminNatID, proctor_national_id= proctorNatID, \
                        AssignedExamRoomID = AssignedExamRoomID)
                    db.classroom_monitoring_db.session.add(newAssignment)
                    db.classroom_monitoring_db.session.commit()
                except KeyError:
                    json.dumps({'status': 'Success', 'message': "exam instance created Successfully!"})

                except NotFound:
                    return json.dumps({'status': 'fail', 'message': "Admin or Proctor or Exam Room ID Not Found"})
                except sqlalchemy.exc.IntegrityError as e:
                    return json.dumps({'status': 'fail', 'message': "Assignment Already Exists"})

                return json.dumps({'status': 'Success', 'message': "Assignment Completed Successfully!"})
        
    # ###############################################################
