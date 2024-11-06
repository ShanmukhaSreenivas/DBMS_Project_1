DROP DATABASE proj1;
CREATE DATABASE proj1;
USE proj1;

-- User Table
CREATE TABLE User (
    user_id VARCHAR(50) PRIMARY KEY, 
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'student', 'ta') NOT NULL
);

-- Admin Table
CREATE TABLE Admin (
    admin_id VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (admin_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Faculty Table
CREATE TABLE Faculty (
    faculty_id VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (faculty_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- ETextbook Table
CREATE TABLE ETextbook (
    textbook_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    admin_id VARCHAR(50) REFERENCES Admin(admin_id) ON DELETE SET NULL,
    faculty_id VARCHAR(50) REFERENCES Faculty(faculty_id) ON DELETE SET NULL
);

-- Course Table
CREATE TABLE Course (
    course_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    faculty_id VARCHAR(50) REFERENCES Faculty(faculty_id) ON DELETE SET NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    course_type ENUM('active', 'evaluation') NOT NULL,
    course_token VARCHAR(7) UNIQUE,
    capacity INTEGER,
    textbook_id INTEGER NOT NULL,
    FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id)
    -- FOREIGN KEY (faculty_id) REFERENCES User(user_id)
);

-- TeachingAssistant Table
CREATE TABLE TeachingAssistant (
    teaching_assistant_id VARCHAR(50) PRIMARY KEY,
    faculty_id VARCHAR(50) REFERENCES Faculty(faculty_id) ON DELETE CASCADE,
    course_id VARCHAR(50) REFERENCES Course(course_id) ON DELETE CASCADE
);

-- Student Table
CREATE TABLE Student (
    student_id VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (student_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Enrollment Table
CREATE TABLE Enrollment (
    enrollment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    course_id VARCHAR(50) NOT NULL REFERENCES Course(course_id) ON DELETE CASCADE,
    student_id VARCHAR(50) NOT NULL REFERENCES Student(student_id) ON DELETE CASCADE,
    total_participation_points INT DEFAULT 0,
    num_of_finished_activities INT DEFAULT 0,
    status ENUM('pending', 'approved') NOT NULL
);

-- Notification Table
CREATE TABLE Notification (
    notification_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    message TEXT NOT NULL,
    user_id VARCHAR(50) NOT NULL REFERENCES User(user_id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- Chapter Table
CREATE TABLE Chapter (
    chapter_id VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    -- chapter_number INTEGER NOT NULL,
    textbook_id INTEGER NOT NULL REFERENCES ETextbook(textbook_id) ON DELETE CASCADE,
    -- UNIQUE (textbook_id, chapter_number),
    hidden ENUM('yes', 'no') NOT NULL DEFAULT 'no',
    PRIMARY KEY (textbook_id, chapter_id)
);

-- Section Table
CREATE TABLE Section (
    section_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    section_number VARCHAR(10) NOT NULL,
    chapter_id VARCHAR(100) NOT NULL,
    textbook_id INTEGER NOT NULL,
    hidden ENUM('yes', 'no') NOT NULL DEFAULT 'no',
    FOREIGN KEY (textbook_id, chapter_id) REFERENCES Chapter(textbook_id, chapter_id) ON DELETE CASCADE,
    UNIQUE (textbook_id, chapter_id, section_number)
);

-- ContentBlock Table
CREATE TABLE ContentBlock (
    content_block_id VARCHAR(50),
    block_type ENUM('text', 'picture', 'activity') NOT NULL DEFAULT 'text',
    content VARCHAR(5000),
    hidden ENUM('yes', 'no') NOT NULL DEFAULT 'no',
    section_id INTEGER NOT NULL REFERENCES Section(section_id) ON DELETE CASCADE,
    PRIMARY KEY (section_id, content_block_id)
);

-- Activity Table
CREATE TABLE Activity (
    activity_id VARCHAR(20),
    hidden ENUM('yes', 'no') NOT NULL DEFAULT 'no',
    section_id INTEGER NOT NULL,
    content_block_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (section_id, content_block_id) REFERENCES ContentBlock(section_id, content_block_id) ON DELETE CASCADE,
    PRIMARY KEY (activity_id, section_id, content_block_id)
);

CREATE TABLE Question(
    question_id VARCHAR(50),
    question_text TEXT NOT NULL,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    explanation1 TEXT,
    explanation2 TEXT,
    explanation3 TEXT,
    explanation4 TEXT,
    correct_option TEXT,
    activity_id VARCHAR(20) NOT NULL,
    section_id INTEGER NOT NULL,
    content_block_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (activity_id,section_id,content_block_id) REFERENCES Activity(activity_id,section_id,content_block_id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, activity_id, section_id, content_block_id)
);

-- Score Table
-- CREATE TABLE Score (
--     score INTEGER NOT NULL,
--     points INTEGER NOT NULL,
--     activity_id VARCHAR(20) NOT NULL REFERENCES Activity(activity_id) ON DELETE CASCADE,
--     student_id VARCHAR(50) NOT NULL REFERENCES Student(student_id) ON DELETE CASCADE,
--     timestamp TIMESTAMP NOT NULL,
--     PRIMARY KEY (activity_id, student_id)
-- );

CREATE TABLE Score (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    textbook_id INT NOT NULL,
    section_id INT NOT NULL,
    chapter_id VARCHAR(50) NOT NULL,
    content_block_id VARCHAR(50) NOT NULL,
    activity_id VARCHAR(50) NOT NULL,
    question_id VARCHAR(50) NOT NULL,
    score INT NOT NULL,
    feedback VARCHAR(255),
    timestamp DATETIME NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES Section(section_id) ON DELETE CASCADE
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
-- VALUES ('blbl2411', 'blah', 'blah2', 'blah@example.com', 'blah', 'admin');

-- SELECT * FROM User;


INSERT INTO User (user_id, first_name, last_name, email, password, role)
VALUES ('blbl2411', 'blah', 'blah2', 'blah@example.com', 'blah', 'admin');

