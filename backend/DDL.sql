use College;
-- CREATE TABLE IF NOT EXISTS student_login(
--    MIS int Primary Key,
--    password varchar(255)
-- );

-- CREATE TABLE IF NOT EXISTS department(
--    deptID varchar(8) primary key,
--    deptName varchar(50) not null
-- );

-- CREATE TABLE IF NOT EXISTS student_account(
--    MIS int Primary Key,
--    firstname varchar(20) not null,
--    lastname varchar(20) not null,
--    email varchar(40) not null,
--    address varchar(400) not null,
--    gender varchar(6) not null,
--    yearEnrolled varchar(4) not null,
--    DOB date not null,
--    deptID varchar(8) not null,
--    profilepic varchar(100) default 'default.png' null,
--    foreign key (MIS) references student_login(MIS) on delete cascade,
--    foreign key (deptID) references department(deptID));

-- insert into department values('comp', 'computer');
-- insert into department values('elec', 'electrical');
-- insert into department values('mech', 'mechanical');
-- insert into department values('civil', 'civil');
-- insert into department values('instru','instrumentation');
-- insert into department values('prod', 'production');
-- insert into department values('meta', 'metallurgy');
-- insert into department values('it', 'information technology');
-- insert into department values('entc', 'electronics & telecommunication');

-- CREATE TABLE IF NOT EXISTS instructor_login(
--    instID int Primary Key,
--    password varchar(255)
-- );


-- CREATE TABLE IF NOT EXISTS instructor_account(
--    instID int Primary Key,
--    firstname varchar(20) not null,
--    lastname varchar(20) not null,
--    email varchar(40) not null,
--    address varchar(400) not null,
--    gender varchar(6) not null,
--    yearEnrolled varchar(4) not null,
--    DOB date not null,
--    deptID varchar(8) not null,
--    profilepic varchar(100) default 'default.png' null,
--    foreign key (instID) references instructor_login(instID) on delete cascade,
--    foreign key (deptID) references department(deptID));

-- CREATE TABLE IF NOT EXISTS course (
--     courseId varchar(20) not null,
--     courseName varchar(40) not null,
--     deptID varchar(8),
--     term varchar(10) not null,
--     credits int,
--     textbook varchar(50),
--     refTextbook varchar(50),
--     courselink varchar(50),
--     maxCap int not null,
--     seatsLeft int not null,
--     primary key (courseId, term),
--     foreign key (deptID) references department(deptID));

-- CREATE TABLE IF NOT EXISTS taken_courses(
--     MIS int,
--     courseId varchar(20) not null);

-- CREATE TABLE IF NOT EXISTS classroom(
--     classID int primary key,
--     loc varchar(12) not null,
--     capacity int,
--     deptID varchar(8),
--     foreign key(deptID) references department(deptID));

-- CREATE TABLE IF NOT EXISTS prereq(
--     prereqId varchar(20) not null primary key,
--     courseId varchar(20) not null,
--     foreign key(courseId) references course(courseId) on delete cascade);

-- CREATE TABLE IF NOT EXISTS taken_in(
--     courseId varchar(20) not null primary key,
--     classID int,
--     foreign key(classID) references classroom(classID) on delete cascade);

-- insert into course values('1001S', 'Artificial Intelligence', 'comp', 'spring', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('2001F', 'EE', 'elec', 'fall', 3, 'None', 'None', 'link', 100, 100);
-- insert into course values('3001F', 'Combustion Engines', 'mech', 'fall', 1, 'None', 'None', 'link', 100, 100);
-- insert into course values('4001S', 'Material Strengths', 'civil', 'spring', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('5001S', 'Control Systems', 'instru', 'spring', 4, 'None', 'None', 'link', 100, 100);
-- insert into course values('1001P', 'Theory of Computation', 'comp', 'spring', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('2001P', 'BEE', 'elec', 'fall', 3, 'None', 'None', 'link', 100, 100);
-- insert into course values('3001P', 'Foundation of ME', 'mech', 'fall', 1, 'None', 'None', 'link', 100, 100);
-- insert into course values('4001P', 'Engg. Mechanics', 'civil', 'spring', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('4001PP', 'Newtonian Mechanics', 'civil', 'spring', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('5001P', 'Sensors and Transducers', 'instru', 'spring', 4, 'None', 'None', 'link', 100, 100);
-- insert into course values('6001F', 'Automation and Robotics', 'prod', 'fall', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('7001S', 'Metals, Alloys and Composites', 'meta', 'spring', 2, 'None', 'None', 'link', 100, 100);
-- insert into course values('8001F', 'IOT Systems', 'it', 'fall', 3, 'None', 'None', 'link', 100, 100);
-- insert into course values('9001F', 'Microprocessors and system arch', 'instru', 'fall', 3, 'None', 'None', 'link', 100, 100);

-- insert into classroom values(101, 'north campus', 110, 'comp');
-- insert into classroom values(102, 'north campus', 120, 'comp');
-- insert into classroom values(103, 'south campus', 80, 'comp');
-- insert into classroom values(201, 'south campus', 90, 'elec');
-- insert into classroom values(202, 'north campus', 100, 'elec');
-- insert into classroom values(301, 'north campus', 100, 'mech');
-- insert into classroom values(302, 'north campus', 130, 'mech');
-- insert into classroom values(401, 'north campus', 80, 'civil');
-- insert into classroom values(402, 'south campus', 100, 'civil');
-- insert into classroom values(501, 'south campus', 110, 'instru');
-- insert into classroom values(502, 'south campus', 90, 'instru');
-- insert into classroom values(601, 'south campus', 110, 'prod');
-- insert into classroom values(602, 'north campus', 90, 'prod');
-- insert into classroom values(701, 'north campus', 100, 'meta');
-- insert into classroom values(702, 'south campus', 100, 'meta');
-- insert into classroom values(801, 'north campus', 100, 'it');

-- insert into prereq values('1001P', '1001S');
-- insert into prereq values('2001P', '2001F');
-- insert into prereq values('3001P', '3001F');
-- insert into prereq values('4001P', '4001S');
-- insert into prereq values('4001PP', '4001P');
-- insert into prereq values('5001P', '5001S');

-- insert into taken_in values('1001S', 101);
-- insert into taken_in values('2001F', 201);
-- insert into taken_in values('3001F', 301);
-- insert into taken_in values('4001S', 401);
-- insert into taken_in values('5001S', 501);
-- insert into taken_in values('1001P', 102);
-- insert into taken_in values('2001P', 201);
-- insert into taken_in values('3001P', 302);
-- insert into taken_in values('4001P', 402);
-- insert into taken_in values('4001PP', 401);
-- insert into taken_in values('5001P', 501);
-- insert into taken_in values('6001F', 601);
-- insert into taken_in values('7001S', 701);
-- insert into taken_in values('8001F', 801);
-- insert into taken_in values('9001F', 402);

CREATE TABLE IF NOT EXISTS handled_by(
   instID int not null,
   courseId varchar(20) primary key,
   foreign key (instID) references instructor_login(instID) on delete cascade,
   foreign key (courseId) references course(courseId) on delete cascade);

insert into handled_by values('11903114','1001P');
insert into handled_by values('11903114','1001S');
insert into handled_by values('11903110','2001F');
insert into handled_by values('11903110','2001P');
insert into handled_by values('11903089','3001F');
insert into handled_by values('11903089','3001P');
insert into handled_by values('11903105','4001P');
insert into handled_by values('11903105','4001PP');
insert into handled_by values('11903105','4001S');
insert into handled_by values('11903014','5001P');
insert into handled_by values('11903014','5001S');
insert into handled_by values('11903115','6001F');
insert into handled_by values('11903073','7001S');
insert into handled_by values('11903118','8001F');
insert into handled_by values('11903014','9001F');









