Classroom Monitoring using AI - Backend

## Entity-Relationship Diagram
![SystemDB-ERD-Copy of chen'sNotation drawio](https://user-images.githubusercontent.com/75078872/161384361-e784dfd9-416a-4525-b548-2b741d4c32c0.png)


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
  ### User-level APIs
    -- /api/user/login_proctor
    -- /api/user/get_assigned_exams
    -- /api/user/choose_model_sensitivity
    -- /api/user/create_possible_case
    -- /api/user/report_case
    -- /api/user/dismiss_case
    -- /api/user/get_frames_links

  ## APIs Detailed Description
    
    ##N.B: Response_data will be returned in all cases, in the cases when no data is returned it will be None. We just added it to maintain consistency to the response payload
    
    -- /api/user/login_proctor
      -- Request Body: 
      {
        "national_id": "",
        "password":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
      

    -- /api/user/get_assigned_exams/<string:proctor_national_id>
      -- Request Body:
      {}
      # Nothing in the request body, proctor_national_id is passed in the url
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   
    -- /api/user/assign_model_sensitivity
      -- Request Body:
      {
        "proctor_national_id":"",
        "exam_instance_id":"",
        "model_sensitivity":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   

    -- /api/user/create_possible_case
      -- Request Body:
      {
        "exam_instance_id":"",
        "stat":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   


    -- /api/user/report_case
      -- Request Body:
      {
        "caseID":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   

    -- /api/user/dismiss_case
      -- Request Body:
        {
          "caseID":""
        }

      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   


    -- /api/user/get_frames_links/<string:caseID>
      -- Request Body:
      {}
      # Nothing in the request body, proctor_national_id is passed in the url

      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   

