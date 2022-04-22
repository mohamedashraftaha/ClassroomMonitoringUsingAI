CREATE DATABASE db;
use db;
CREATE TABLE admin(
national_id VARCHAR(255) NOT NULL PRIMARY KEY,
passwd VARCHAR(255) NOT NULL ,
first_name VARCHAR(255) NOT NULL,
last_name VARCHAR(255) NOT NULL,
job_role VARCHAR(255) NOT NULL
);

CREATE TABLE exam_instance(
exam_instance_id VARCHAR(255) NOT NULL PRIMARY KEY,
exam_reference_code VARCHAR(255) NOT NULL,
ts datetime default current_timestamp ,
school_name VARCHAR(255) NOT NULL,
admin_national_id VARCHAR(255) NOT NULL,
camera_static_ip VARCHAR(255) NOT NULL,
FOREIGN KEY (admin_national_id) REFERENCES admin(national_id)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE proctor(
national_id VARCHAR(255) NOT NULL PRIMARY KEY,
passwd VARCHAR(255) NOT NULL ,
first_name VARCHAR(255) NOT NULL,
last_name VARCHAR(255) NOT NULL,
school_name VARCHAR(255) NOT NULL
);

CREATE TABLE admin_assign_proctor(
admin_national_id VARCHAR(255) NOT NULL ,
proctor_national_id VARCHAR(255) NOT NULL,
ts datetime default current_timestamp,
exam_instance_id VARCHAR(255) NOT NULL,
PRIMARY KEY(admin_national_id,proctor_national_id, exam_instance_id), 
FOREIGN KEY (proctor_national_id ) REFERENCES proctor(national_id)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (admin_national_id) REFERENCES admin(national_id)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (exam_instance_id) REFERENCES exam_instance(exam_instance_id)
ON UPDATE CASCADE ON DELETE CASCADE
);

create TABLE proctor_monitor_exam(
proctor_national_id VARCHAR(255) NOT NULL,
exam_instance_id VARCHAR(255) NOT NULL,
model_sensitivity VARCHAR(255) NOT NULL DEFAULT "50%",
PRIMARY KEY(proctor_national_id, exam_instance_id),
FOREIGN KEY (proctor_national_id ) REFERENCES admin_assign_proctor(proctor_national_id)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (exam_instance_id) REFERENCES admin_assign_proctor(exam_instance_id)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE exam_instance_cases(
case_id int,
exam_instance_id VARCHAR(255) NOT NULL,
stat VARCHAR(255) NOT NULL DEFAULT "Pending",
confidence double NOT NULL,
ts datetime default current_timestamp,
PRIMARY KEY(case_id, exam_instance_id),
FOREIGN KEY (exam_instance_id) REFERENCES exam_instance(exam_instance_id)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE frames(
image_link VARCHAR(512) NOT NULL PRIMARY KEY,
case_id int ,
FOREIGN KEY (case_id) REFERENCES exam_instance_cases(case_id)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE students_positions(
student_number int NOT NULL ,
exam_instance_id VARCHAR(255) NOT NULL,
x double NOT NULL DEFAULT 0.0,
y double NOT NULL DEFAULT 0.0,
w double NOT NULL DEFAULT 0.0,
h double NOT NULL DEFAULT 0.0,
PRIMARY KEY(student_number, exam_instance_id)
FOREIGN KEY (exam_instance_id) REFERENCES exam_instance(exam_instance_id)
ON UPDATE CASCADE ON DELETE CASCADE
);