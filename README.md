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

## System Workflow

![systemWorkflow drawio](https://user-images.githubusercontent.com/75078872/165160857-1dfc9138-f4d7-4527-8351-b1121b8b3656.svg)




## System Communication Diagram


![SystemCommunicationDiagram drawio](https://user-images.githubusercontent.com/75078872/165157241-eebba353-be3c-42dd-b92c-69923682d2e7.png)

[SystemCommunicationDiagram.drawio.pdf](https://github.com/mohamedashraftaha/ClassroomMonitoringUsingAI/files/8557313/SystemCommunicationDiagram.drawio.pdf)

## Frontend

## Backend

### Tools
* Python
* Flask
* MySQL
* MySQL Workbench
* AWS S3 Bucket
* OpenAPI Specification "Swagger"

### Entity-Relationship Diagram
![SystemDB-ERD-Copy of chen'sNotation drawio](https://user-images.githubusercontent.com/75078872/165162620-17b249e5-99e9-4fab-af45-e1df53949511.svg)

### APIs
  #### Admin-level APIs
    -- /api/admin/register_admin
    -- /api/admin/login_admin
    -- /api/admin/create_exam_instance
    -- /api/admin/assign_proctor_to_exam
    -- /api/admin/register_proctor
    -- /api/admin/add_students_to_exam
    

#### User-level APIs
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
    


  ### APIs Detailed Description
  
  http://classroommonitoring.herokuapp.com/
   

  

  


## Model


  

   

