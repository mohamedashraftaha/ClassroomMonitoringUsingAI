# Classroom Monitoring Using AI


![index](https://user-images.githubusercontent.com/75078872/152257154-ae82bd7f-ac67-4245-865e-8eb8261bb4cd.png)

Department of Computer Science and Engineering

## Supervisiors
   Our Thesis project is supervised by:
   * Dr. Sherif Aly
   * Dr. Hesham Eraqi

## Team Members
   * Noha Abdelkader
      * Undergraduate Graduating senior student at The American University in Cairo
   * Mohamed Ashraf Taha 
      * Undergraduate Graduating senior student at The American University in Cairo
   * Marwan Awad 
      * Undergraduate Graduating senior student at The American University in Cairo
   * Mohamed Elshabshiri 
      * Undergraduate Graduating senior student at The American University in Cairo
   * Omar Mahdy
      * Undergraduate Graduating senior student at The American University in Cairo
   * Youssef Beshir
      * Undergraduate Graduating senior student at The American University in Cairo
   
   

## Problem Statement
   Based on our research we found that The increasing rates of cheating during examinations in Egypt, that results in an unfair educational experience.
   
## Proposed Solution
   Developing a classroom monitoring system using AI to detect possible cheating incidents during examinations that creates fair and safe examination environment 

# System
![image](https://user-images.githubusercontent.com/75078872/165158725-f17ffb51-9407-4484-984a-53e3de802e66.png)


## Software Requirements
* Python>=3.8
* Flask
* ElectronJS
* Npm
* MySQL
* MySQL Workbench
* AWS S3 Bucket
* AWS EC2


## System Communication Diagram


![SystemCommunicationDiagram drawio](https://user-images.githubusercontent.com/75078872/165157241-eebba353-be3c-42dd-b92c-69923682d2e7.png)

[SystemCommunicationDiagram.drawio.pdf](https://github.com/mohamedashraftaha/ClassroomMonitoringUsingAI/files/8557313/SystemCommunicationDiagram.drawio.pdf)

## Frontend

## Backend
Classroom Monitoring using AI - Backend

## Entity-Relationship Diagram
![SystemDB-ERD-Copy of chen'sNotation drawio](https://user-images.githubusercontent.com/75078872/161384383-e91ad16c-689c-496a-b1c5-54777b168c3c.png)


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
    -- /api/user/get_assigned_exams/<string:proctor_national_id>
    -- /api/user/assign_model_sensitivity
    -- /api/user/create_possible_case
    -- /api/user/report_case
    -- /api/user/dismiss_case
    -- /api/user/get_frames_links/<string:caseID>
    -- /api/user/get_exam_instance_details/<string:examInstanceID>

  ## APIs Detailed Description
    
    ##N.B: Response_data will be returned in all cases, in the cases when no data is returned it will be None. We just added it to maintain consistency to the response payload
    
    A. -- /api/user/login_proctor
      -- Request Body: 
      {
        "national_id": "",
        "password":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
      

    B.-- /api/user/get_assigned_exams/<string:proctor_national_id>
      -- Request Body:
      {}
      # Nothing in the request body, proctor_national_id is passed in the url
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   
    C.-- /api/user/assign_model_sensitivity
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
   

    D-- /api/user/create_possible_case
      -- Request Body:
      {
        "exam_instance_id":"",
        "stat":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   


    E-- /api/user/report_case
      -- Request Body:
      {
        "caseID":""
      }
      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   

    F-- /api/user/dismiss_case
      -- Request Body:
        {
          "caseID":""
        }

      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   


    G-- /api/user/get_frames_links/<string:caseID>
      -- Request Body:
      {}
      # Nothing in the request body, proctor_national_id is passed in the url

      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   

    H--   api/user/get_exam_instance_details/<string:examInstanceID>
      -- Request Body:
      {}
      # Nothing in the request body, examInstanceID is passed in the url

      -- Response
        {
          'status': status, 'msg': msg, 'data': responseData
        }
   

  


## Model


  

   

