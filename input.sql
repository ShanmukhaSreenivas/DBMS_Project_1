
USE proj1;

INSERT INTO ETextbook (textbook_id, title) VALUES
(101, 'Database Management Systems'),
(102, 'Fundamentals of Software Engineering'),
(103, 'Fundamentals of Machine Learning');


INSERT INTO Chapter (textbook_id, chapter_id, title, hidden) VALUES
(101, 'chap01', 'Introduction to Database', 'no'),
(101, 'chap02', 'The Relational Model', 'no'),
(102, 'chap01', 'Introduction to Software Engineering', 'no'),
(102, 'chap02', 'Introduction to Software Development Life Cycle (SDLC)', 'no'),
(103, 'chap01', 'Introduction to Machine Learning', 'no');


INSERT INTO Section (textbook_id, chapter_id, section_number, title, hidden) VALUES
(101, 'chap01', 'Sec01', 'Database Management Systems (DBMS) Overview', 'no'),
(101, 'chap01', 'Sec02', 'Data Models and Schemas', 'no'),
(101, 'chap02', 'Sec01', 'Entities, Attributes, and Relationships', 'no'),
(101, 'chap02', 'Sec02', 'Normalization and Integrity Constraints', 'no'),
(102, 'chap01', 'Sec01', 'History and Evolution of Software Engineering', 'no'),
(102, 'chap01', 'Sec02', 'Key Principles of Software Engineering', 'no'),
(102, 'chap02', 'Sec01', 'Phases of the SDLC', 'yes'),
(102, 'chap02', 'Sec02', 'Agile vs. Waterfall Models', 'no'),
(103, 'chap01', 'Sec01', 'Overview of Machine Learning', 'yes'),
(103, 'chap01', 'Sec02', 'Supervised vs Unsupervised Learning', 'no');




-- Insert content blocks into ContentBlock table by referencing section_id through a subquery
INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec01' LIMIT 1),
    'Block01', 'text', 'A Database Management System (DBMS) is software that enables users to efficiently create, manage, and manipulate databases.', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
    'Block01', 'activity', 'ACT0', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap02' AND section_number = 'Sec01' LIMIT 1),
    'Block01', 'text', 'DBMS systems provide structured storage and ensure that data is accessible through queries using languages like SQL.', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap02' AND section_number = 'Sec02' LIMIT 1),
    'Block01', 'picture', 'sample.png', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec01' LIMIT 1),
    'Block01', 'text', 'The history of software engineering dates back to the 1960s...', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
    'Block01', 'activity', 'ACT0', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap02' AND section_number = 'Sec01' LIMIT 1),
    'Block01', 'text', 'The Software Development Life Cycle (SDLC) consists of key phases...', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap02' AND section_number = 'Sec02' LIMIT 1),
    'Block01', 'picture', 'sample2.png', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec01' LIMIT 1),
    'Block01', 'text', 'Machine learning is a subset of artificial intelligence...', 'no'
);


INSERT INTO ContentBlock (section_id, content_block_id, block_type, content, hidden)
VALUES (
    (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
    'Block01', 'activity', 'ACT0', 'no'
);






INSERT INTO Activity (activity_id, hidden, section_id, content_block_id)
VALUES 
('ACT0', 'no', 
    (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1), 
    'Block01'
);


INSERT INTO Activity (activity_id, hidden, section_id, content_block_id)
VALUES 
('ACT0', 'no', 
    (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) , 
    'Block01'
);


INSERT INTO Activity (activity_id, hidden, section_id, content_block_id)
VALUES 
('ACT0', 'no', 
    (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1), 
    'Block01'
);




-- Questions for textbook_id = 101, chapter_id = chap01, section_number = Sec02
INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q1', 'What does a DBMS provide?', 
 'Data storage only', 'Incorrect: DBMS provides more than just storage', 
 'Data storage and retrieval', 'Correct: DBMS manages both storing and retrieving data', 
 'Only security features', 'Incorrect: DBMS also handles other functions', 
 'Network management', 'Incorrect: DBMS does not manage network infrastructure', 
 '2', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
  (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
  'Block01'
);


INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q2', 'Which of these is an example of a DBMS?', 
 'Microsoft Excel', 'Incorrect: Excel is a spreadsheet application', 
 'MySQL', 'Correct: MySQL is a popular DBMS', 
 'Google Chrome', 'Incorrect: Chrome is a web browser', 
 'Windows 10', 'Incorrect: Windows is an operating system', 
 '2', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
  (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
  'Block01'
);


-- Questions for textbook_id = 101, chapter_id = chap01, section_number = Sec02
INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q3', 'What type of data does a DBMS manage?', 
 'Structured data', 'Correct: DBMS primarily manages structured data', 
 'Unstructured multimedia', 'Incorrect: While some DBMS systems can handle it, it\'s not core', 
 'Network traffic data', 'Incorrect: DBMS doesn’t manage network data', 
 'Hardware usage statistics', 'Incorrect: DBMS does not handle hardware usage data', 
 '1', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);

-- Questions for textbook_id = 102, chapter_id = chap01, section_number = Sec02
INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q1', 'What was the "software crisis"?', 
 'A hardware shortage', 'Incorrect: The crisis was related to software development issues', 
 'Difficulty in software creation', 'Correct: The crisis was due to the complexity and unreliability of software', 
 'A network issue', 'Incorrect: It was not related to networking', 
 'Lack of storage devices', 'Incorrect: The crisis was not about physical storage limitations', 
 '2', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);

INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q2', 'Which methodology was first introduced in software engineering?', 
 'Waterfall model', 'Correct: Waterfall was the first formal software development model', 
 'Agile methodology', 'Incorrect: Agile was introduced much later', 
 'DevOps', 'Incorrect: DevOps is a more recent development approach', 
 'Scrum', 'Incorrect: Scrum is a part of Agile, not the first methodology', 
 '1', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);

INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q3', 'What challenge did early software engineering face?', 
 'Lack of programming languages', 'Incorrect: Programming languages existed but were difficult to manage', 
 'Increasing complexity of software', 'Correct: Early engineers struggled with managing large, complex systems', 
 'Poor hardware development', 'Incorrect: The issue was primarily with software, not hardware', 
 'Internet connectivity issues', 'Incorrect: Internet connectivity wasn\'t a challenge in early software', 
 '2', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);

-- Questions for textbook_id = 103, chapter_id = chap01, section_number = Sec02
INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q1', 'What is the primary goal of supervised learning?', 
 'Predict outcomes', 'Correct: The goal is to learn a mapping from inputs to outputs for prediction.', 
 'Group similar data', 'Incorrect: This is more aligned with unsupervised learning.', 
 'Discover patterns', 'Incorrect: This is not the main goal of supervised learning.', 
 'Optimize cluster groups', 'Incorrect: This is not applicable to supervised learning.', 
 '1', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);

INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q2', 'Which type of data is used in unsupervised learning?', 
 'Labeled data', 'Incorrect: Unsupervised learning uses unlabeled data.', 
 'Unlabeled data', 'Correct: It analyzes data without pre-existing labels.', 
 'Structured data', 'Incorrect: Unlabeled data can be structured or unstructured.', 
 'Time-series data', 'Incorrect: Unsupervised learning does not specifically focus on time-series.', 
 '2', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);

INSERT INTO Question (question_id, question_text, option1, explanation1, option2, explanation2, option3, explanation3, option4, explanation4, correct_option, activity_id, section_id, content_block_id)
VALUES 
('Q3', 'In which scenario would you typically use supervised learning?', 
 'Customer segmentation', 'Incorrect: This is more relevant to unsupervised learning.', 
 'Fraud detection', 'Correct: Supervised learning is ideal for predicting fraud based on labeled examples.', 
 'Market basket analysis', 'Incorrect: This is generally done using unsupervised methods.', 
 'Anomaly detection', 'Incorrect: While applicable, it is less common than fraud detection in supervised learning.', 
 '2', 
 (SELECT activity_id FROM Activity 
  WHERE section_id = (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1) 
  AND content_block_id = 'Block01'),
 (SELECT section_id FROM Section WHERE textbook_id = 103 AND chapter_id = 'chap01' AND section_number = 'Sec02' LIMIT 1),
 'Block01'
);






-- Faculty:
INSERT INTO User (user_id, first_name, last_name, email, password, role) VALUES
('KeOg1024', 'Kemafor', 'Ogan', 'kogan@ncsu.edu', 'Ko2024!rpc', 'faculty'),
('JoDo1024', 'John', 'Doe', 'john.doe@example.com', 'Jd2024!abc', 'faculty'),
('SaMi1024', 'Sarah', 'Miller', 'sarah.miller@domain.com', 'Sm#Secure2024', 'faculty'),
('DaBr1024', 'David', 'Brown', 'david.b@webmail.com', 'DbPass123!', 'faculty'),
('EmDa1024', 'Emily', 'Davis', 'emily.davis@email.com', 'Emily#2024!', 'faculty'),
('MiWi1024', 'Michael', 'Wilson', 'michael.w@service.com', 'Mw987secure', 'faculty');


INSERT INTO Faculty (faculty_id) VALUES
('KeOg1024'),
('JoDo1024'),
('SaMi1024'),
('DaBr1024'),
('EmDa1024'),
('MiWi1024');




-- TA:


INSERT INTO User (user_id, first_name, last_name, email, password, role) VALUES
('JaWi1024', 'James', 'Williams', 'jwilliams@ncsu.edu', 'jwilliams@1234', 'ta'),
('LiAl0924', 'Lisa', 'Alberti', 'lalberti@ncsu.edu', 'lalberti&5678@', 'ta'),
('DaJo1024', 'David', 'Johnson', 'djohnson@ncsu.edu', 'djohnson%@1122', 'ta'),
('ElCl1024', 'Ellie', 'Clark', 'eclark@ncsu.edu', 'eclark^#3654', 'ta'),
('JeGi0924', 'Jeff', 'Gibson', 'jgibson@ncsu.edu', 'jgibson$#9877', 'ta');




-- Courses:
INSERT INTO Course (course_id, title, textbook_id, course_type, faculty_id, start_date, end_date, course_token, capacity)
VALUES 
('NCSUOganCSC440F24', 'CSC440 Database Systems', 101, 'active', 'KeOg1024', '2024-08-15', '2024-12-15', 'XYJKLM', 60),
('NCSUOganCSC540F24', 'CSC540 Database Systems', 101, 'active', 'KeOg1024', '2024-08-17', '2024-12-15', 'STUKZT', 50),
('NCSUSaraCSC326F24', 'CSC326 Software Engineering', 102, 'active', 'SaMi1024', '2024-08-23', '2024-10-23', 'LRUFND', 100),
('NCSUDoeCSC522F24', 'CSC522 Fundamentals of Machine Learning', 103, 'evaluation', 'JoDo1024', '2025-08-25', '2025-12-18', NULL, NULL),
('NCSUSaraCSC326F25', 'CSC326 Software Engineering', 102, 'evaluation', 'SaMi1024', '2025-08-27', '2025-12-19', NULL, NULL);

INSERT INTO TeachingAssistant (teaching_assistant_id, course_id, faculty_id) VALUES
('JaWi1024', 'NCSUOganCSC440F24', 'KeOg1024'),
('LiAl0924', 'NCSUOganCSC540F24', 'KeOg1024'),
('DaJo1024', 'NCSUSaraCSC326F24', 'SaMi1024'),
('ElCl1024', NULL, NULL),
('JeGi0924', NULL, NULL);


-- Student:


INSERT INTO User (user_id, first_name, last_name, email, password, role) VALUES
('ErPe1024', 'Eric', 'Perrig', 'ez356@example.mail', 'qwdmq', 'student'),
('AlAr1024', 'Alice', 'Artho', 'aa23@edu.mail', 'omdsws', 'student'),
('BoTe1024', 'Bob', 'Temple', 'bt163@template.mail', 'sak+=', 'student'),
('LiGa1024', 'Lily', 'Gaddy', 'li123@example.edu', 'cnaos', 'student'),
('ArMo1024', 'Aria', 'Morrow', 'am213@example.edu', 'jwocals', 'student'),
('KeRh1014', 'Kellan', 'Rhodes', 'kr21@example.edu', 'camome', 'student'),
('SiHa1024', 'Sienna', 'Hayes', 'sh13@example.edu', 'asdqm', 'student'),
('FiWi1024', 'Finn', 'Wilder', 'fw23@example.edu', 'f13mas', 'student'),
('LeMe1024', 'Leona', 'Mercer', 'lm56@example.edu', 'ca32', 'student');


INSERT INTO Student (student_id) VALUES
('ErPe1024'),
('AlAr1024'),
('BoTe1024'),
('LiGa1024'),
('ArMo1024'),
('KeRh1014'),
('SiHa1024'),
('FiWi1024'),
('LeMe1024');

INSERT INTO Enrollment (course_id, student_id, status) VALUES 
('NCSUOganCSC440F24', 'ErPe1024', 'approved'),
('NCSUOganCSC540F24', 'ErPe1024', 'approved'),
('NCSUOganCSC440F24', 'AlAr1024', 'approved'),
('NCSUOganCSC440F24', 'BoTe1024', 'approved'),
('NCSUOganCSC440F24', 'LiGa1024', 'approved'),
('NCSUOganCSC540F24', 'LiGa1024', 'approved'),
('NCSUOganCSC540F24', 'ArMo1024', 'approved'),
('NCSUOganCSC440F24', 'ArMo1024', 'approved'),
('NCSUOganCSC440F24', 'SiHa1024', 'approved'),
('NCSUSaraCSC326F24', 'FiWi1024', 'approved'),
('NCSUOganCSC440F24', 'LeMe1024', 'approved'),
('NCSUOganCSC440F24', 'FiWi1024', 'pending'),
('NCSUOganCSC540F24', 'LeMe1024', 'pending'),
('NCSUOganCSC540F24', 'AlAr1024', 'pending'),
('NCSUOganCSC540F24', 'SiHa1024', 'pending'),
('NCSUOganCSC540F24', 'FiWi1024', 'pending');




INSERT INTO Enrollment (course_id, student_id, status, total_participation_points, num_of_finished_activities) VALUES
('NCSUOganCSC440F24', 'ErPe1024', 'approved', 4, 2),
('NCSUOganCSC540F24', 'ErPe1024', 'approved', 1, 1),
('NCSUOganCSC440F24', 'AlAr1024', 'approved', 3, 1),
('NCSUOganCSC440F24', 'BoTe1024', 'approved', 0, 1),
('NCSUOganCSC440F24', 'LiGa1024', 'approved', 9, 3),
('NCSUOganCSC540F24', 'LiGa1024', 'approved', 0, 0),
('NCSUOganCSC540F24', 'ArMo1024', 'approved', 0, 0),
('NCSUOganCSC440F24', 'ArMo1024', 'approved', 4, 2),
('NCSUOganCSC440F24', 'SiHa1024', 'approved', 0, 0),
('NCSUSaraCSC326F24', 'FiWi1024', 'approved', 1, 1);


INSERT INTO Score (student_id, course_id, textbook_id, section_id, chapter_id, content_block_id, activity_id, question_id, score, timestamp)
VALUES
('ErPe1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 3, '2024-08-01 11:10:00'),
('ErPe1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q2', 1, '2024-08-01 14:18:00'),
('ErPe1024', 'NCSUOganCSC540F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 1, '2024-08-02 19:06:00'),
('AlAr1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 3, '2024-08-01 13:24:00'),
('BoTe1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 0, '2024-08-01 09:24:00'),
('LiGa1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 3, '2024-08-01 07:45:00'),
('LiGa1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q2', 3, '2024-08-01 12:30:00'),
('LiGa1024', 'NCSUOganCSC540F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 3, '2024-08-03 16:52:00'),
('ArMo1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 1, '2024-08-01 21:18:00'),
('ArMo1024', 'NCSUOganCSC440F24', 101, 
 (SELECT section_id FROM Section WHERE textbook_id = 101 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q2', 3, '2024-08-01 05:03:00'),
('FiWi1024', 'NCSUSaraCSC326F24', 102, 
 (SELECT section_id FROM Section WHERE textbook_id = 102 AND chapter_id = 'chap01' AND section_number = 'Sec02'),
 'chap01', 'Block01', 'ACT0', 'Q1', 1, '2024-08-29 22:41:00');