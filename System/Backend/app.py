# imports all dependencies
from __init__ import *
from controllers import  userController, adminController
from admin_panel import *



'''This python file is responsible for putting everything together and
starting the application'''
#this variable will be used to store passwords in the DB
salt = None



'''Creating views for the database tables in the admin panel
i.e:modelling how the tables' attributes will be displayed in the admin panel'''
a.add_view(MyModelView(db.admin, db.classroom_monitoring_db.session,endpoint='adminstrator',form_columns=['national_id', 'passwd', 'first_name','last_name','job_role'] ))    
a.add_view(MyModelView(db.proctor, db.classroom_monitoring_db.session,form_columns=['national_id', 'passwd', 'first_name','last_name','school_name']  ))
a.add_view(MyModelView(db.exam_instance, db.classroom_monitoring_db.session,form_columns=['exam_instance_id', 'exam_reference_code', 'school_name','admin_national_id','camera_static_ip','fps']  ))
a.add_view(MyModelView(db.admin_assign_proctor, db.classroom_monitoring_db.session,form_columns=['admin_national_id', 'proctor_national_id', 'exam_instance_id']  ))
a.add_view(MyModelView(db.proctor_monitor_exam, db.classroom_monitoring_db.session,form_columns=['proctor_national_id', 'exam_instance_id', 'model_sensitivity']  ))
a.add_view(MyModelView(db.exam_instance_cases, db.classroom_monitoring_db.session,form_columns=['case_id', 'exam_instance_id', 'stat','confidence','student_number']  ))
a.add_view(MyModelView(db.frames, db.classroom_monitoring_db.session,form_columns=['image_link', 'case_id','student_number','exam_instance_id']  ))
a.add_view(MyModelView(db.students_positions, db.classroom_monitoring_db.session,form_columns=['student_number', 'exam_instance_id', 'x','y','w','h']  ))

if __name__ == '__main__':
    user_level_api = userController.UserLevelAPIs()
    admin_level_api = adminController.AdminLevelAPIs()            
    #DEBUG is SET to TRUE. CHANGE FOR PROD

    app.run(debug=True, host='0.0.0.0')
    session.clear()
