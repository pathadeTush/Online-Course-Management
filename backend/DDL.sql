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