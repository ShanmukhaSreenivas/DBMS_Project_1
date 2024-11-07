-- Retrieval SQL Queries
USE proj1;
-- 1. Write a query that prints the number of sections of the first chapter of a textbook.
SELECT COUNT(s.section_id) FROM section s
JOIN etextbook e ON e.textbook_id = s.textbook_id
JOIN chapter c ON c.chapter_id = s.chapter_id
AND c.textbook_id = s.textbook_id
WHERE
e.textbook_id = '101'-- 'Enter the Textbook ID here'
AND c.chapter_id = 'chap01'; 

-- 2. Print the names of faculty and TAs of all courses. For each person print their role next to their names. 
SELECT 
t.course_id AS 'Course',
CONCAT(u.first_name, " ", u.last_name) AS 'Name',
u.role as 'Role'
FROM user u
JOIN teachingassistant t
ON (t.faculty_id = u.user_id OR t.teaching_assistant_id = u.user_id)
WHERE t.course_id IS NOT NULL
ORDER BY t.course_id ASC, u.role ASC;


-- 3. For each active course, print the course id, faculty member and total number of students
SELECT
c.course_id AS 'Course ID',
f.faculty_id AS 'Faculty Member',
CONCAT(u.first_name, " ", u.last_name) AS 'Faculty Member Name',
COUNT(s.student_id) 'Total Number of Students'
FROM course c
JOIN faculty f ON f.faculty_id = c.faculty_id
JOIN user u ON u.user_id = f.faculty_id
JOIN enrollment e ON e.course_id = c.course_id
JOIN student s ON s.student_id = e.student_id
WHERE
c.course_type = 'active'
AND e.status = 'approved'
GROUP BY c.course_id;

-- 4. Find the course which the largest waiting list, print the course id and the total number of people on the list
SELECT course_id 'Course ID', wc 'Waitlist Count'
FROM (SELECT c1.course_id, COUNT(s1.student_id) AS 'wc'
FROM course c1
JOIN enrollment e1 ON e1.course_id = c1.course_id
JOIN student s1 ON s1.student_id = e1.student_id
WHERE e1.status = 'pending'
GROUP BY c1.course_id
ORDER BY COUNT(s1.student_id) DESC) wait_table
WHERE 1=1 LIMIT 1;

-- 5. Print the contents of Chapter 02 of textbook 101 in proper sequence.
SELECT e.textbook_id AS 'Book ID',
e.title AS 'Book Title',
c.chapter_id AS 'Chapter ID',
c.title AS 'Chapter Title',
s.section_number AS 'Section Number',
s.title AS 'Title',
cb.content_block_id AS 'Content Block ID',
cb.block_type AS 'Block Type',
cb.content AS 'Block Content',
cb.hidden AS 'Is Content Block Hidden',
a.activity_id AS 'Activity ID',
a.hidden AS 'Is Activity Hidden',
q.question_id AS 'Question ID',
q.question_text AS 'Question Text',
q.option1 AS 'Option 1',
q.option2 AS 'Option 2',
q.option3 AS 'Option 3',
q.option4 AS 'Option 4',
q.explanation1 AS 'Explanation 1',
q.explanation2 AS 'Explanation 2',
q.explanation3 AS 'Explanation 3',
q.explanation4 AS 'Explanation 4',
q.correct_option AS 'Correct Option'

FROM 
etextbook e
JOIN chapter c
ON e.textbook_id = c.textbook_id
JOIN section s
ON s.chapter_id = c.chapter_id
AND s.textbook_id = c.textbook_id
LEFT JOIN contentblock cb
ON (cb.section_id = s.section_id)
LEFT JOIN activity a
ON (a.content_block_id = cb.content_block_id
AND a.section_id = s.section_id)
LEFT JOIN question q
ON (q.activity_id = a.activity_id
AND q.content_block_id = cb.content_block_id
AND q.section_id = s.section_id)

WHERE 1=1
AND c.chapter_id = 'chap02'
AND e.textbook_id = '101';

-- 6. For Q2 of Activity0, print the incorrect answers for that question and their corresponding explanations.
SELECT 
s.textbook_id AS 'Textbook ID',
q.question_id AS 'Question ID',
q.question_text AS 'Question Text',
(CASE 
WHEN (q.correct_option = '2' OR q.correct_option = '3' OR q.correct_option = '4') 
THEN CONCAT("Option 1 : ", q.option1) 
ELSE CONCAT("Option 2 : ", q.option2) 
END) AS 'Incorrect Option 1',
(CASE 
WHEN (q.correct_option = '2' OR q.correct_option = '3' OR q.correct_option = '4') 
THEN CONCAT("Explanation 1 : ", q.explanation1) 
ELSE CONCAT("Explanation 2 : ", q.explanation2) 
END) AS 'Incorrect Explanation 1',
(CASE 
WHEN (q.correct_option = '1' OR q.correct_option = '2')
THEN CONCAT("Option 3 : ", q.option3)  
WHEN (q.correct_option = '3' OR q.correct_option = '4') 
THEN CONCAT("Option 2 : ", q.option2)  
END) AS 'Incorrect Option 2',
(CASE 
WHEN (q.correct_option = '1' OR q.correct_option = '2')
THEN CONCAT("Explanation 3 : ", q.explanation3)  
WHEN (q.correct_option = '3' OR q.correct_option = '4') 
THEN CONCAT("Explanation 2 : ", q.explanation2)  
END) AS 'Incorrect Explanation 2',
(CASE
WHEN (q.correct_option = '1' OR q.correct_option = '2' OR q.correct_option = '3')
THEN CONCAT("Option 4 : ", q.option4)
WHEN q.correct_option = '4'
THEN CONCAT("Option 3 : ", q.option3) 
END) AS 'Incorrect Option 3',
(CASE
WHEN (q.correct_option = '1' OR q.correct_option = '2' OR q.correct_option = '3')
THEN CONCAT("Explanation 4 : ", q.explanation4)
WHEN q.correct_option = '4'
THEN CONCAT("Explanation 3 : ", q.explanation3) 
END) AS 'Incorrect Option 3'

FROM question q 
JOIN Activity a
ON q.activity_id = a.activity_id 
AND q.section_id = a.section_id 
AND q.content_block_id = a.content_block_id
JOIN section s
ON s.section_id = a.section_id

WHERE 1=1
AND q.question_id = 'Q2' AND q.activity_id = 'ACT0';


-- 7. Find any book that is in active status by one instructor but evaluation status by a different instructor.
SELECT
DISTINCT
e.textbook_id AS 'Textbook ID',
e.title AS 'Textbook Title'
FROM etextbook e
WHERE 
e.textbook_id IN 
(SELECT e1.textbook_id
FROM etextbook e1
JOIN course c1
ON c1.textbook_id = e1.textbook_id
JOIN course c2
ON c2.textbook_id = e1.textbook_id
AND c1.course_type = 'active'
AND c2.course_type = 'evaluation');

