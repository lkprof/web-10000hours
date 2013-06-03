create table users(
	user_id int auto_increment,
	name varchar(20),
	email varchar(30),
	password varchar(20),
	sex varchar(4),
	primary key(user_id)
);

create table subjects(
	subject_id int auto_increment,
	subject_user_id int,
	title varchar(20),
	content varchar(20),
	posted_on datetime,
	primary key(subject_id),
	foreign key(subject_user_id) references users(user_id)
);

create table spend_on_subject(
	spend_id int auto_increment,
	spend_subject_id int,
	spend_time int,
	summary text,
	posted_on datetime,
	primary key(spend_id),
	foreign key(spend_subject_id) references subjects(subject_id)
);
insert into users set name='admin',password='admin',email='ad@gmail.com',sex='f';
insert into subjects (subject_user_id,title,content,posted_on) values (1,'learn swimming','everyday',now());
insert into spend_on_subject (spend_subject_id,spend_time,summary,posted_on) values (1,5.5,'not enough',now());
select subjects.title,subjects.subject_id,subjects.posted_on,spend_time from spend_on_subject,subjects,users 
where users.user_id=subjects.subject_user_id and subjects.subject_id=spend_on_subject.spend_subject_id;

drop table spend_on_subject;
drop table subjects;
drop table users;