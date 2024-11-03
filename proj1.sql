CREATE DATABASE project_db;
USE project_db;
-- User Table
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
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
    admin_id INTEGER REFERENCES Admin(admin_id) ON DELETE SET NULL
);

CREATE TABLE ETextbook_Access (
    etextbook_id INTEGER,
    user_id INTEGER,
    access_level ENUM('customize', 'view') NOT NULL,
    PRIMARY KEY (etextbook_id, user_id),
    FOREIGN KEY (etextbook_id) REFERENCES ETextbook(textbook_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Course Table
CREATE TABLE Course (
    course_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    faculty_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    course_type ENUM('active', 'evaluation') NOT NULL,
    course_token VARCHAR(7) NOT NULL,
    capacity INTEGER NOT NULL,
    textbook_id INTEGER,
    FOREIGN KEY (faculty_id) REFERENCES Faculty(faculty_id) ON DELETE SET NULL,
    FOREIGN KEY (textbook_id) REFERENCES ETextbook(textbook_id) ON DELETE SET NULL
);

-- TeachingAssistant Table
CREATE TABLE TeachingAssistant (
    teaching_assistant_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL REFERENCES User(user_id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES Course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (teaching_assistant_id) REFERENCES User(user_id) ON DELETE CASCADE
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
    score_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    score INTEGER NOT NULL,
    points INTEGER NOT NULL,
    activity_id INTEGER NOT NULL REFERENCES Activity(activity_id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES Student(student_id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL
);

-- Step 1: Insert a new user as an admin
INSERT INTO User (first_name, last_name, email, password)
VALUES ('Test', 'Admin', 'testadmin@example.com', 'adminpassword');

-- Step 2: Get the user_id of the new admin
SELECT user_id FROM User WHERE email = 'testadmin@example.com';

-- Step 3: Use the retrieved user_id to insert into the Admin table
-- Assuming user_id obtained from previous step is, say, 1
INSERT INTO Admin (admin_id) VALUES (1);

-- Add a sample faculty
INSERT INTO User (first_name, last_name, email, password)
VALUES ('Test', 'Faculty', 'testfaculty@example.com', 'facultypassword');

-- Get the user_id for the faculty user
SELECT user_id FROM User WHERE email = 'testfaculty@example.com';

-- Assuming faculty's user_id is 2, add this to Faculty table
INSERT INTO Faculty (faculty_id) VALUES (2);

-- Add a sample e-textbook with admin ownership
INSERT INTO ETextbook (title, admin_id) VALUES ('Sample E-Textbook', 1);

-- Add a sample course linked to the sample faculty and e-textbook
INSERT INTO Course (title, faculty_id, start_date, end_date, course_type, course_token, capacity, textbook_id)
VALUES ('Sample Active Course', 2, '2024-01-01', '2024-06-01', 'active', 'ABC1234', 30, 1);



