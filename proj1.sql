CREATE DATABASE proj1;
USE proj1;

-- User Table
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'student', 'ta') NOT NULL
);

-- Admin Table
CREATE TABLE Admin (
    admin_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    FOREIGN KEY (admin_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Faculty Table
CREATE TABLE Faculty (
    faculty_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    FOREIGN KEY (faculty_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- ETextbook Table
CREATE TABLE ETextbook (
    textbook_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    admin_id INTEGER REFERENCES Admin(admin_id) ON DELETE SET NULL,
    faculty_id INTEGER REFERENCES Faculty(faculty_id) ON DELETE SET NULL
);

-- Course Table
CREATE TABLE Course (
    course_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    faculty_id INTEGER REFERENCES Faculty(faculty_id) ON DELETE SET NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    course_type ENUM('active', 'evaluation') NOT NULL,
    course_token VARCHAR(7) NOT NULL,
    capacity INTEGER NOT NULL,
    textbook_id INTEGER NOT NULL,
    FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id),
    FOREIGN KEY (faculty_id) REFERENCES User(user_id)
);

-- TeachingAssistant Table
CREATE TABLE TeachingAssistant (
    teaching_assistant_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL REFERENCES User(user_id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES Course(course_id) ON DELETE CASCADE
);

-- Student Table
CREATE TABLE Student (
    student_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    FOREIGN KEY (student_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Enrollment Table
CREATE TABLE Enrollment (
    enrollment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    course_id INTEGER NOT NULL REFERENCES Course(course_id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES Student(student_id) ON DELETE CASCADE,
    status ENUM('pending', 'approved') NOT NULL
);

-- Notification Table
CREATE TABLE Notification (
    notification_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    message TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES User(user_id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- Chapter Table
CREATE TABLE Chapter (
    chapter_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    chapter_number INTEGER NOT NULL,
    textbook_id INTEGER NOT NULL REFERENCES ETextbook(textbook_id) ON DELETE CASCADE,
    UNIQUE (textbook_id, chapter_number)
);

-- Section Table
CREATE TABLE Section (
    section_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    section_number INTEGER NOT NULL,
    chapter_id INTEGER NOT NULL REFERENCES Chapter(chapter_id) ON DELETE CASCADE,
    UNIQUE (chapter_id, section_number)
);

-- ContentBlock Table
CREATE TABLE ContentBlock (
    content_block_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    block_type VARCHAR(50) NOT NULL,
    content ENUM('text', 'image') NOT NULL,
    hidden TINYINT,
    section_id INTEGER NOT NULL REFERENCES Section(section_id) ON DELETE CASCADE
);

-- Activity Table
CREATE TABLE Activity (
    activity_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    incorrect_answer1 TEXT NOT NULL,
    incorrect_answer2 TEXT NOT NULL,
    incorrect_answer3 TEXT NOT NULL,
    explanation TEXT NOT NULL,
    content_block_id INTEGER NOT NULL REFERENCES ContentBlock(content_block_id) ON DELETE CASCADE
);

-- Score Table
CREATE TABLE Score (
    score INTEGER NOT NULL,
    points INTEGER NOT NULL,
    activity_id INTEGER NOT NULL REFERENCES Activity(activity_id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES Student(student_id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (activity_id, student_id)
);



-- -- 1st query
-- -- Replace 'TextbookID' with the ID of a text book
-- SELECT COUNT(*) AS NumberOfSections
-- FROM section
-- WHERE chapter_id = (
--     SELECT chapter_id
--     FROM chapter
--     WHERE textbook_id = [TextbookID] AND chapter_number = 1
-- );

-- -- 2nd query:
-- (SELECT 
-- 	Course.title AS CourseTitle,
-- 	CONCAT(User.first_name, ' ', User.last_name) AS UserName,
-- 	User.role AS UserRole 
-- FROM Faculty
-- JOIN Course ON Faculty.faculty_id = Course.faculty_id
-- JOIN User ON Faculty.faculty_id = User.user_id)

-- UNION

-- (SELECT 
--     Course.title AS CourseTitle,
--     CONCAT(User.first_name, ' ', User.last_name) AS UserName,
--     User.role AS UserRole 
-- FROM TeachingAssistant
-- JOIN Course ON TeachingAssistant.course_id = Course.course_id
-- JOIN User ON TeachingAssistant.user_id = User.user_id);

-- INSERT INTO User (user_id, first_name, last_name, email, password, role)
-- VALUES ('1', 'blah', 'blah2', 'blah@example.com', 'blah', 'admin');

