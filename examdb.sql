create DATABASE examdb;
use examdb;

create table account(
	acc_id int not null Unique Primary Key auto_increment,
    role varchar(7) not null,
    name varchar(255) not null,
    email varchar(255) not null,
    password char(8) not null
);
create table test(
		test_id int not null Unique Primary Key auto_increment,
		title varchar(40) not null,
		created_by int not null Unique,
    foreign key (created_by) references account(acc_id)
);
create table question(
		question_id int not null Unique Primary Key auto_increment,
        test_id int not null Unique,
        question_text text not null,
	foreign key (test_id) references test(test_id)
);
create table submission(
		submission_id int not null Unique Primary Key auto_increment,
        acc_id int not null Unique,
        test_id int not null Unique,
	foreign key (acc_id) references account(acc_id),
    foreign key (test_id) references test(test_id)
);
create table answer(
		answer_id int not null Unique Primary Key auto_increment,
        submission_id int not null Unique,
        question_id int not null Unique,
        answer_text text not null,
	foreign key (submission_id) references submission(submission_id),
    foreign key (question_id) references question(question_id)
);
create table grade(
		grade_id int not null Unique Primary Key auto_increment,
        submission_id int not null Unique,
        acc_id int not null Unique,
        mark int,
	foreign key (submission_id) references submission(submission_id),
    foreign key (acc_id) references account(acc_id)
);