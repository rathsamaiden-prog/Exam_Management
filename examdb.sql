drop database examdb;

create database examdb;
use examdb;

create table account(
	acc_id int not null Unique Primary Key auto_increment,
    role varchar(7) not null,
    name varchar(255) not null,
    email varchar(255) not null,
    password char(8) not null
) ENGINE=InnoDB;
create table test(
		test_id int not null Primary Key auto_increment,
		title varchar(40) not null,
		created_by int not null,
    foreign key (created_by) references account(acc_id)
) ENGINE=InnoDB;
create table question(
		question_id int not null Primary Key auto_increment,
        test_id int not null,
        question_text text not null,
	foreign key (test_id) references test(test_id) ON DELETE CASCADE
) ENGINE=InnoDB;
create table submission(
		submission_id int not null Unique Primary Key auto_increment,
        acc_id int not null,
        test_id int not null,
	foreign key (acc_id) references account(acc_id),
    foreign key (test_id) references test(test_id) ON DELETE CASCADE
) ENGINE=InnoDB;
create table answer(
		answer_id int not null Primary Key auto_increment,
        submission_id int not null,
        question_id int not null,
        answer_text text not null,
	foreign key (submission_id) references submission(submission_id) ON DELETE CASCADE,
    foreign key (question_id) references question(question_id) On DELETE CASCADE
) ENGINE=InnoDB;
create table grade(
		grade_id int not null Unique Primary Key auto_increment,
        submission_id int not null,
        acc_id int not null,
        mark int,
	foreign key (submission_id) references submission(submission_id) ON DELETE CASCADE,
    foreign key (acc_id) references account(acc_id)
) ENGINE=InnoDB;

