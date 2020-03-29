create table course(
	courseID character(8) primary key,
    room character(5),
    subject character(10)

);

create table student(
	id character(10) primary key,
    given character(10), 
    family character(10)

);

create table enroll(
	stuID character(10),
	courseID character(10),
	lab_mark numeric(3),
	exam_mark numeric(3),
    foreign key (stuID) references student (id) on update cascade,
	foreign key (courseID) references course (id) on update cascade    

);


insert into course values (100, 2, 'Databases');
insert into course values (101, 3, 'Networking');
insert into course values (200, 'Rob', 'Halford');
insert into course values (201, 'Nicko', 'McBrain');
insert into course enroll (200, 100); 
