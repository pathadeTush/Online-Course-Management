use College;
CREATE TABLE IF NOT EXISTS student_login(
   MIS int Primary Key,
   password varchar(255));

CREATE TABLE IF NOT EXISTS department(
   deptID varchar(8) primary key,
   deptName varchar(50) not null);

CREATE TABLE IF NOT EXISTS student_account(
   MIS int Primary Key,
   firstname varchar(20) not null,
   lastname varchar(20) not null,
   email varchar(40) not null,
   address varchar(400) not null,
   gender varchar(6) not null,
   yearEnrolled varchar(4) not null,
   DOB date not null,
   deptID varchar(8) not null,
   profilepic varchar(100) default 'default.png' null,
   foreign key (MIS) references student_login(MIS) on delete cascade,
   foreign key (deptID) references department(deptID));

CREATE TABLE IF NOT EXISTS instructor_login(
   instID int Primary Key,
   password varchar(255));

CREATE TABLE IF NOT EXISTS instructor_account(
   instID int Primary Key,
   firstname varchar(20) not null,
   lastname varchar(20) not null,
   email varchar(40) not null,
   address varchar(400) not null,
   gender varchar(6) not null,
   yearEnrolled varchar(4) not null,
   DOB date not null,
   deptID varchar(8) not null,
   profilepic varchar(100) default 'default.png' null,
   foreign key (instID) references instructor_login(instID) on delete cascade,
   foreign key (deptID) references department(deptID));

CREATE TABLE IF NOT EXISTS course (
   courseId varchar(20) not null,
   courseName varchar(200) not null,
   deptID varchar(8),
   term varchar(10) not null,
   credits int,
   textbook varchar(400),
   refTextbook varchar(400),
   courselink varchar(50),
   maxCap int not null,
   seatsLeft int not null,
   primary key (courseId, term),
   foreign key (deptID) references department(deptID));

CREATE TABLE IF NOT EXISTS taken_courses(
   MIS int, 
   courseId varchar(20) not null,
   foreign key (MIS) references student_account(MIS) on delete cascade,
   foreign key(courseId) references course(courseId) on delete cascade);

CREATE TABLE IF NOT EXISTS classroom(
   classID int primary key,
   loc varchar(12) not null,
   capacity int,
   deptID varchar(8),
   foreign key(deptID) references department(deptID));

CREATE TABLE IF NOT EXISTS prereq(
   prereqId varchar(20) not null primary key,
   courseId varchar(20) not null,
   foreign key(prereqId) references course(courseId) on delete cascade,
   foreign key(courseId) references course(courseId) on delete cascade);

CREATE TABLE IF NOT EXISTS taken_in(
   courseId varchar(20) not null primary key,
   classID int,
   foreign key(classID) references classroom(classID) on delete cascade,
   foreign key(courseId) references course(courseId) on delete cascade);

CREATE TABLE IF NOT EXISTS handled_by(
   instID int not null,
   courseId varchar(20) primary key,
   foreign key (instID) references instructor_login(instID) on delete cascade,
   foreign key (courseId) references course(courseId) on delete cascade);

-- Department entries
insert into department values('comp', 'computer');
insert into department values('elec', 'electrical');
insert into department values('mech', 'mechanical');
insert into department values('civil', 'civil');
insert into department values('instru','instrumentation');
insert into department values('prod', 'production');
insert into department values('meta', 'metallurgy');

-- Course entries
-- Comp
insert into course values('CS1001', 'Artificial Intelligence', 'comp', 'spring', 2, 'Artificial Intelligence – A Modern Approach', 'The Elements of Statistical Learning', 'link', 100, 100);
insert into course values('CS1002', 'Computer Networks', 'comp', 'spring', 3, 'Computer Networking A Top Down Approach', 'Foundations of Python Network Programming', 'link', 100, 100);
insert into course values('CS1003', 'Database Management', 'comp', 'fall', 3, 'Database system concepts by Silberschatz, Korth and Sudarshan', 'Fundamentals of Database Systems', 'link', 100, 100);
insert into course values('CS1004', 'Computer Architecture', 'comp', 'spring', 3, 'Computer Architecture: A Quantitative Approach', 'Computer Organization and Design', 'link', 100, 100);

-- Elec
insert into course values('EE1001', 'Electro-magnetism', 'elec', 'spring', 2, 'Electricity and Magnetism', 'A Treatise on Electricity and Magnetism', 'link', 100, 100);
insert into course values('EE1002', 'Control systems', 'elec', 'fall', 3, 'Automatic Control Systems', 'Modern Control Systems', 'link', 100, 100);
insert into course values('EE1003', 'Embedded Systems', 'elec', 'fall', 3, 'The Art of Designing Embedded Systems', 'An Embedded Software Primer', 'link', 100, 100);
insert into course values('EE1004', 'Intelligent Systems', 'elec', 'spring', 3, 'Building Intelligent Systems', 'Intelligent Systems: A Modern Approach Ajith Abraham', 'link', 100, 100);

-- Mech
insert into course values('ME1001', 'Engineering Mechanics', 'mech', 'spring', 3, 'Engineering Mechanics: Statics', 'Vector mechanics for engineers', 'link', 100, 100);
insert into course values('ME1002', 'Heat Transfer', 'mech', 'fall', 2, 'Introduction to Heat Transfer', 'Fundamentals of Heat and Mass Transfer', 'link', 100, 100);
insert into course values('ME1003', 'Machine Drawing', 'mech', 'fall', 2, 'A Textbook of Machine Drawing', 'MACHINE DRAWING Ajeet Singh', 'link', 100, 100);
insert into course values('ME1004', 'Fluid Mechanics', 'mech', 'spring', 3, 'A Textbook of Fluid Mechanics and Hydraulic Machines', 'Introduction to Fluid Mechanics and Fluid Machines', 'link', 100, 100);

-- Civil
insert into course values('CE1001', 'Bridge Engineering', 'civil', 'spring', 2, 'Bridge Engineering Demetrios Tonias', 'Bridge Engineering S. C. Rangwala', 'link', 100, 100);
insert into course values('CE1002', 'Land development', 'civil', 'fall', 3, 'Residential land development practices', 'Be a Successful Residential Land Developer', 'link', 100, 100);
insert into course values('CE1003', 'Transportation engineering', 'civil', 'spring', 3, 'Transportation Engineering and Planning', 'Transportation Engineering: An Introduction', 'link', 100, 100);
insert into course values('CE1004', 'Hydraulic Engineering', 'civil', 'fall', 2, 'Fundamentals of Hydraulic Engineering Systems', 'Hydraulic Engineering M. Hanif Chaudhry', 'link', 100, 100);

-- Instru
insert into course values('IE1001', 'Control Systems and Process Control', 'instru', 'spring', 2, 'Process control systems F. Shinskey', 'Industrial Process Control Systems Dale R. Patrick', 'link', 100, 100);
insert into course values('IE1002', 'Electrical and Electronic Measurements', 'instru', 'fall', 2, 'Electrical Measurements and Measuring Instruments', 'Electronic Measurements and Instrumentation R.K. Rajput', 'link', 100, 100);
insert into course values('IE1003', 'Analog Electronic', 'instru', 'spring', 3, 'Principles of Analog Electronics', 'Electronic Devices and Circuit Theory', 'link', 100, 100);
insert into course values('IE1004', 'Digital Electronics', 'instru', 'spring', 3, 'Digital Electronics: Principles, Devices and Applications', 'Modern Digital Electronics', 'link', 100, 100);


-- Prod
insert into course values('PE1001', 'Materials Science and Engineering', 'prod', 'spring', 2, 'Materials Science and Engineering: An Introduction', 'Foundations of materials science and engineering', 'link', 100, 100);
insert into course values('PE1002', 'Manufacturing Planning and Control', 'prod', 'fall', 3, 'Introduction To Manufacturing Planning and Control Systems', 'Foundations of Manufacturing Planning', 'link', 100, 100);
insert into course values('PE1003', 'Quality Design And Control', 'prod', 'spring', 3, 'Introduction To Quality Design And Control', 'Process Control: Principles And Application', 'link', 100, 100);
insert into course values('PE1004', 'Introduction to Machine Learning in Production', 'prod', 'spring', 3, 'Dive into Deep Learning', 'Designing Data-Intensive Applications', 'link', 100, 100);

-- Meta
insert into course values('MT1001', 'Fluid Flow and Heat Transfer', 'meta', 'spring', 2, 'Numerical heat transfer and fluid flow', 'Computational Fluid Mechanics and Heat Transfer', 'link', 100, 100);
insert into course values('MT1002', 'Geology and Minerals Beneficiation', 'meta', 'spring', 2, 'Mineral Beneficiation: A Concise Basic Course', 'Geological Structures and Maps A Practical Guide', 'link', 100, 100);
insert into course values('MT1003', 'Electrical Technology-A', 'meta', 'fall', 3, 'A Textbook Of Electrical Technology', 'Introduction To Electrical Technology', 'link', 100, 100);
insert into course values('MT1004', 'Mathematics-IIIN', 'meta', 'fall', 3, 'A First Course In Abstract Algebra By Fraleigh', 'Foundation Of Mathematics-IIIN', 'link', 100, 100);


-- Prereq entries
insert into prereq values('CS1001', 'CS1002');
insert into prereq values('CS1003', 'CS1002');
insert into prereq values('EE1001', 'EE1002');
insert into prereq values('EE1004', 'EE1003');
insert into prereq values('ME1004', 'ME1003');
insert into prereq values('CE1002', 'CE1003');
insert into prereq values('IE1001', 'IE1004');
insert into prereq values('PE1003', 'PE1004');
insert into prereq values('MT1004', 'MT1002');
insert into prereq values('MT1001', 'ME1003');

-- Handled_by entries

-- Comp
insert into handled_by values('119030','CS1001');
insert into handled_by values('119030','CS1002');
insert into handled_by values('119031','CS1003');
insert into handled_by values('119031','CS1004');

--Elec
insert into handled_by values('119040','EE1001');
insert into handled_by values('119040','EE1002');
insert into handled_by values('119041','EE1003');
insert into handled_by values('119041','EE1004');

--Mech
insert into handled_by values('119050','ME1001');
insert into handled_by values('119050','ME1002');
insert into handled_by values('119051','ME1003');
insert into handled_by values('119051','ME1004');

-- Civil
insert into handled_by values('119060','CE1001');
insert into handled_by values('119060','CE1002');
insert into handled_by values('119061','CE1003');
insert into handled_by values('119061','CE1004');

-- Instru
insert into handled_by values('119070','IE1001');
insert into handled_by values('119070','IE1002');
insert into handled_by values('119071','IE1003');
insert into handled_by values('119071','IE1004');

-- Prod
insert into handled_by values('119080','PE1001');
insert into handled_by values('119080','PE1002');
insert into handled_by values('119081','PE1003');
insert into handled_by values('119081','PE1004');

-- Meta
insert into handled_by values('119090','MT1001');
insert into handled_by values('119090','MT1002');
insert into handled_by values('119091','MT1003');
insert into handled_by values('119091','MT1004');

-- Classroom entries

insert into classroom values(101, 'north campus', 110, 'comp');
insert into classroom values(102, 'north campus', 120, 'comp');
insert into classroom values(103, 'south campus', 80, 'comp');
insert into classroom values(104, 'south campus', 90, 'comp');
insert into classroom values(201, 'south campus', 90, 'elec');
insert into classroom values(202, 'north campus', 100, 'elec');
insert into classroom values(203, 'north campus', 90, 'elec');
insert into classroom values(204, 'south campus', 80, 'elec');
insert into classroom values(301, 'north campus', 100, 'mech');
insert into classroom values(302, 'south campus', 80, 'mech');
insert into classroom values(303, 'north campus', 130, 'mech');
insert into classroom values(304, 'south campus', 90, 'mech');
insert into classroom values(401, 'north campus', 80, 'civil');
insert into classroom values(402, 'south campus', 100, 'civil');
insert into classroom values(403, 'north campus', 90, 'civil');
insert into classroom values(404, 'south campus', 100, 'civil');
insert into classroom values(501, 'south campus', 110, 'instru');
insert into classroom values(502, 'north campus', 90, 'instru');
insert into classroom values(503, 'north campus', 100, 'instru');
insert into classroom values(504 'south campus', 90, 'instru');
insert into classroom values(601, 'south campus', 110, 'prod');
insert into classroom values(602, 'north campus', 90, 'prod');
insert into classroom values(603, 'south campus', 100, 'prod');
insert into classroom values(604, 'south campus', 110, 'prod');
insert into classroom values(701, 'north campus', 100, 'meta');
insert into classroom values(702, 'south campus', 90, 'meta');
insert into classroom values(703, 'north campus', 100, 'meta');
insert into classroom values(704, 'south campus', 80, 'meta');

-- Instructor Account entries

    insert into instructor_account values('119030', 'Mahendra', 'Dhoni', 'md@coep.ac.in', 'COEP hostel, Pune', 'male', '2001', '10/2/1976');
    insert into instructor_account values('119031', 'Virat', 'Kohli', 'vk@coep.ac.in', 'COEP hostel, Pune', 'male', '2000', '1/3/1969');
    insert into instructor_account values('119040', 'Ravi', 'Jadeja', 'ej@coep.ac.in', 'COEP hostel, Pune', 'male', '2000', '21/4/1974');
    insert into instructor_account values('119041', 'Rohit', 'Sharma', 'rs@coep.ac.in', 'COEP hostel, Pune', 'male', '2002', '11/5/1980');
    insert into instructor_account values('119050', 'Shikhar', 'Dhawan', 'sd@coep.ac.in', 'COEP hostel, Pune', 'male', '2002', '17/6/1983');
    insert into instructor_account values('119051', 'Rishabh', 'Pant', 'rp@coep.ac.in', 'COEP hostel, Pune', 'male', '2003', '18/7/1987');
    insert into instructor_account values('119060', 'Hardik', 'Pandya', 'hp@coep.ac.in', 'COEP hostel, Pune', 'male', '2003', '16/8/1971');
    insert into instructor_account values('119061', 'Siddharth', 'Kaul', 'sk@coep.ac.in', 'COEP hostel, Pune', 'male', '2003', '14/9/1973');
    insert into instructor_account values('119070', 'Ishant', 'Sharma', 'is@coep.ac.in', 'COEP hostel, Pune', 'male', '2002', '20/10/1974');
    insert into instructor_account values('119071', 'Yuzi', 'Chahal', 'yc@coep.ac.in', 'COEP hostel, Pune', 'male', '2003', '22/11/1975');
    insert into instructor_account values('119080', 'Mohd.', 'Shami', 'ms@coep.ac.in', 'COEP hostel, Pune', 'male', '2002', '31/12/1982');
    insert into instructor_account values('119081', 'Ajinkya', 'Rahane', 'ar@coep.ac.in', 'COEP hostel, Pune', 'male', '2000', '6/1/1985');
    insert into instructor_account values('119090', 'Rahul', 'Dravid', 'rd@coep.ac.in', 'COEP hostel, Pune', 'male', '2001', '3/2/1986');
    insert into instructor_account values('119091', 'Sachin', 'Tendulkar', 'st@coep.ac.in', 'COEP hostel, Pune', 'male', '2001', '19/3/1988');



-- Taken_in entries

-- Comp
insert into taken_in values('CS1001', 101);
insert into taken_in values('CS1002', 102);
insert into taken_in values('CS1003', 103);
insert into taken_in values('CS1004', 104);

--Elec
insert into taken_in values('EE1001', 201);
insert into taken_in values('EE1002', 202);
insert into taken_in values('EE1003', 203);
insert into taken_in values('EE1004', 204);

--Mech
insert into taken_in values('ME1001', 301);
insert into taken_in values('ME1002', 302;
insert into taken_in values('ME1003', 303);
insert into taken_in values('ME1004', 304);

-- Civil
insert into taken_in values('CE1001', 401);
insert into taken_in values('CE1002', 402);
insert into taken_in values('CE1003', 403);
insert into taken_in values('CE1004', 404);

-- Instru
insert into taken_in values('IE1001', 501);
insert into taken_in values('IE1002', 502);
insert into taken_in values('IE1003', 503);
insert into taken_in values('IE1004', 504);

-- Prod
insert into taken_in values('PE1001', 601);
insert into taken_in values('PE1002', 602);
insert into taken_in values('PE1003', 603);
insert into taken_in values('PE1004', 604);

-- Meta
insert into taken_in values('MT1001', 701);
insert into taken_in values('MT1002', 702);
insert into taken_in values('MT1003', 703);
insert into taken_in values('MT1004', 704);



--  FOLLOWING ARE PREVIOUS ONES DONT USE THEM DIRECTLY


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

-- insert into handled_by values('11903114','1001P');
-- insert into handled_by values('11903114','1001S');
-- insert into handled_by values('11903110','2001F');
-- insert into handled_by values('11903110','2001P');
-- insert into handled_by values('11903089','3001F');
-- insert into handled_by values('11903089','3001P');
-- insert into handled_by values('11903105','4001P');
-- insert into handled_by values('11903105','4001PP');
-- insert into handled_by values('11903105','4001S');
-- insert into handled_by values('11903014','5001P');
-- insert into handled_by values('11903014','5001S');
-- insert into handled_by values('11903115','6001F');
-- insert into handled_by values('11903073','7001S');
-- insert into handled_by values('11903118','8001F');
-- insert into handled_by values('11903014','9001F');