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

![systemWorkflow drawio(3)](https://user-images.githubusercontent.com/75078872/168029579-42157eed-4653-475b-9e5b-78ae81b26849.png)




## System Communication Diagram


![SystemCommunicationDiagram drawio](https://user-images.githubusercontent.com/75078872/165157241-eebba353-be3c-42dd-b92c-69923682d2e7.png)

[SystemCommunicationDiagram.drawio.pdf](https://github.com/mohamedashraftaha/ClassroomMonitoringUsingAI/files/8557313/SystemCommunicationDiagram.drawio.pdf)

## Frontend
The system’s front end has been designed to fulfill the users’ needs by developing multiple UI/UX designs before starting the development process. In addition to building a system design to effectively communicate with the system’s backend represented in the database and the Application Programming Interfaces (APIs) connecting it. 
The software is a cross-platform desktop application that supports multiple operating systems: Linux, macOS, and Microsoft Windows. ElectronJS is a JavaScript framework that uses web development technologies such as HTML5, CSS3, Bootstrap 5, and JavaScript. It has been used to build cross-platform desktop applications and has been chosen to be the frontend development framework for our software, as it has high performance on different platforms, in addition to a smooth and quick development process due to having one code base for the three supported operating systems. 
The software consists of  7 frontend interfaces that communicate with a total of 9 Application Programming interfaces (APIs). The frontend interfaces are as follows:

* Software Landing Page.
* User Login Page.
* Assigned Exam Details Page.
* Exam Sensitivity Page.
* Main Home Page.
* End of Exam Report Page.
* User Logout Page.

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


  

   

