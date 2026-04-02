use examdb;

INSERT INTO account (role, name, email, password) VALUES
('teacher', 'Alice Johnson', 'alice@test.edu', 'pass1234'),
('teacher', 'David Lee', 'david@test.edu', 'pass1234'),
('student', 'Bob Smith', 'bob@test.edu', 'pass1234'),
('student', 'Charlie Brown', 'charlie@test.edu', 'pass1234'),
('student', 'Emma Davis', 'emma@test.edu', 'pass1234');

INSERT INTO test (title, created_by) VALUES
('Math Quiz', 1),
('History Test', 2);

INSERT INTO question (test_id, question_text) VALUES
-- Math Quiz (test_id = 1)
(1, 'What is 2 + 2?'),
(1, 'What is 10 / 2?'),
(1, 'What is 3 * 4?');

INSERT INTO question (test_id, question_text) VALUES
-- History Test (test_id = 2)
(2, 'Who was the first president of the USA?'),
(2, 'What year did World War II end?'),
(2, 'What empire was ruled by Julius Caesar?');

INSERT INTO submission (acc_id, test_id) VALUES
(3, 1),  -- Bob takes Math
(4, 1),  -- Charlie takes Math
(5, 2),  -- Emma takes History
(3, 2);  -- Bob also takes History

INSERT INTO answer (submission_id, question_id, answer_text) VALUES
-- Bob (submission 1 - Math)
(1, 1, '4'),
(1, 2, '5'),
(1, 3, '12');
INSERT INTO answer (submission_id, question_id, answer_text) VALUES
-- Charlie (submission 2 - Math)
(2, 1, '4'),
(2, 2, '5'),
(2, 3, '12');
INSERT INTO answer (submission_id, question_id, answer_text) VALUES
-- Emma (submission 3 - History)
(3, 4, 'George Washington'),
(3, 5, '1945'),
(3, 6, 'Roman Empire');
INSERT INTO answer (submission_id, question_id, answer_text) VALUES
-- Bob (submission 4 - History)
(4, 4, 'Washington'),
(4, 5, '1945'),
(4, 6, 'Rome');

select * from account;
select * from answer;
select * from grade;
select * from question;
select * from submission;
select * from test;

DELETE from submission where submission_id = 12;
