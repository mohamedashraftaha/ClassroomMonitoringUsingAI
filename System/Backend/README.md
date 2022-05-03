Classroom Monitoring using AI - Backend

## Tools
* Python
* Flask
* MySQL
* MySQL Workbench
* AWS S3 Bucket
* OpenAPI Specification "Swagger"

## Entity-Relationship Diagram
![SystemDB-ERD-Copy of chen'sNotation drawio](https://user-images.githubusercontent.com/75078872/165162620-17b249e5-99e9-4fab-af45-e1df53949511.svg)


## Relational Model
  * admin(national_id, first_name, last_name, job_role, password)

  * exam_instance(exam_instance_id, school_name, exam_reference_code, timestamp, camera_static_ip, admin_national_id)

  * proctor(national_id, first_name, last_name, school_name, password)

  * camera(availability, static_ip)  → LATER
  
  * admin_assign_proctor(admin_national_id, proctor_national_id, exam_instance_id,ts)
  
  * proctor_monitor_exam(proctor_national_id, exam_instance_id, model_sensitivity)
  
  * exam_instance_cases(case_id, stat,  timestamp, exam_instance_id)
  
  * frames(image_link, case_id)

## APIs
  ### Admin-level APIs
    -- /api/admin/register_admin
    -- /api/admin/login_admin
    -- /api/admin/create_exam_instance
    -- /api/admin/assign_proctor_to_exam
    -- /api/admin/register_proctor
    -- /api/admin/add_students_to_exam
    

### User-level APIs
    -- /api/user/add_students_locations
    -- /api/user/assign_model_sensitivity
    -- /api/user/dismiss_case
    -- /api/user/generate_exam_report
    -- /api/user/get_assigned_exams/{proctor_national_id}
    -- /api/user/get_exam_instance_details/{examInstanceID}
    -- /api/user/get_fps/{exam_instance_id}
    -- /api/user/get_frames_links/{caseID}/{exam_instance_id}
    -- /api/user/get_recent_case/{exam_instance_id}
    -- /api/user/login_proctor
    -- /api/user/report_case
    


  ## APIs Detailed Description
  
  http://classroommonitoring.herokuapp.com/
   

  
