create database to_do_app;
use to_do_app

create table tasks (task_name varchar(1000),
status DEFAULT=0,
important int DEFAULT=0,
due_date date,
id int NOT NULL PRIMARY KEY auto_increment,
due_time time NOT NULL ,
google_id varchar(40) );


