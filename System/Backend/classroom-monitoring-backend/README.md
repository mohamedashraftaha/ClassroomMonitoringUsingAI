Classroom Monitoring using AI - Backend

## Entity-Relationship Diagram
![SystemDB-ERD-Copy of chen'sNotation drawio](https://user-images.githubusercontent.com/75078872/161354145-801ec27e-ec65-45d1-b967-3377ac52e0a4.png)


## Relational Model
  * admin(national_id, first_name, last_name, job_role, password)

  * exam_instance(exam_instance_id, school_name, exam_reference_code, timestamp, camera_static_ip, admin_national_id)

  * proctor(national_id, first_name, last_name, school_name, password, exam_instance_id)

  * camera(availability, static_ip)

  * admin_assign_proctor(admin_national_id, proctor_national_id, exam_instance_id)

  * exam_instance_cases(case_id, timestamp, exam_instance_id)

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
