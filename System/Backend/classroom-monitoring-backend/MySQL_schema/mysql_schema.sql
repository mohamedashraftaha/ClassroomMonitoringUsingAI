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
PRIMARY KEY(admin_national_id,proctor_national_id), 
FOREIGN KEY (proctor_national_id ) REFERENCES proctor(national_id)
ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY (admin_national_id) REFERENCES admin(national_id)
ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE exam_instance_cases(
case_id int NOT NULL AUTO_INCREMENT,
exam_instance_id VARCHAR(255) NOT NULL,
stat VARCHAR(255) NOT NULL DEFAULT 'Not Cheating',
ts datetime default current_timestamp,
PRIMARY KEY(case_id, exam_instance_id),
FOREIGN KEY (exam_instance_id) REFERENCES exam_instance(exam_instance_id)
ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE frames(
image_link VARCHAR(255) NOT NULL PRIMARY KEY,
case_id int NOT NULL DEFAULT 0,
FOREIGN KEY (case_id) REFERENCES exam_instance_cases(case_id)
ON UPDATE CASCADE ON DELETE CASCADE
);