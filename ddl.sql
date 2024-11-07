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


USE proj1
-- Stored procedure for hiding a chapter

DELIMITER //

CREATE PROCEDURE hide_chapter(IN p_chapter_id VARCHAR(100), IN p_textbook_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Failed: An error occurred while hiding the chapter.' AS ErrorMessage;
    END;

    START TRANSACTION;
    UPDATE Chapter
    SET hidden = 'yes'
    WHERE chapter_id = p_chapter_id AND textbook_id = p_textbook_id;
    
    COMMIT;
    SELECT CONCAT('Success: Chapter ', p_chapter_id, ' has been hidden.') AS SuccessMessage;
END //

DELIMITER ;


-- Stored procedure for deleting a chapter

DELIMITER //

CREATE PROCEDURE delete_chapter(IN p_chapter_id VARCHAR(100), IN p_textbook_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Failed: An error occurred while deleting the chapter.' AS ErrorMessage;
    END;

    START TRANSACTION;
    DELETE FROM Chapter
    WHERE chapter_id = p_chapter_id AND textbook_id = p_textbook_id;
    
    COMMIT;
    SELECT CONCAT('Success: Chapter ', p_chapter_id, ' has been deleted.') AS SuccessMessage;
END //

DELIMITER ;

-- Stored procedure for hiding a section

DELIMITER //

CREATE PROCEDURE hide_section(IN p_section_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Failed: An error occurred while hiding the section.' AS ErrorMessage;
    END;

    START TRANSACTION;
    UPDATE Section
    SET hidden = 'yes'
    WHERE section_id = p_section_id;

    COMMIT;
    SELECT CONCAT('Success: Section ', p_section_id, ' has been hidden.') AS SuccessMessage;
END //

DELIMITER ;


-- Stored procedure for deleting a section

DELIMITER //

CREATE PROCEDURE delete_section(IN p_section_id INT)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Failed: An error occurred while deleting the section.' AS ErrorMessage;
    END;

    START TRANSACTION;
    DELETE FROM Section
    WHERE section_id = p_section_id;

    COMMIT;
    SELECT CONCAT('Success: Section ', p_section_id, ' has been deleted.') AS SuccessMessage;
END //

DELIMITER ;



USE proj1
-- Automatically Hide All Sections When a Chapter is Hidden

DELIMITER //

CREATE TRIGGER hide_sections_after_chapter_hidden
AFTER UPDATE ON Chapter
FOR EACH ROW
BEGIN
    IF NEW.hidden = 'yes' THEN
        UPDATE Section SET hidden = 'yes' WHERE chapter_id = NEW.chapter_id;
    END IF;
END //

DELIMITER ;

-- Automatically Delete Related Sections When a Chapter is Deleted
DELIMITER //

CREATE TRIGGER delete_sections_before_chapter
BEFORE DELETE ON Chapter
FOR EACH ROW
BEGIN
    DELETE FROM Section WHERE chapter_id = OLD.chapter_id;
END //

DELIMITER ;

-- Validation for chapter_id Format
DELIMITER //

CREATE TRIGGER validate_chapter_id
BEFORE INSERT ON Chapter
FOR EACH ROW
BEGIN
    IF NEW.chapter_id NOT REGEXP '^chap[0-9][1-9]$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: chapter_id must be in the format chap[0-9][1-9]';
    END IF;
END //

DELIMITER ;

-- Validation for section_number Format

DELIMITER //

CREATE TRIGGER validate_section_number
BEFORE INSERT ON Section
FOR EACH ROW
BEGIN
    IF NEW.section_number NOT REGEXP '^sec[0-9][1-9]$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: section_number must be in the format sec[0-9][1-9]';
    END IF;
END //

DELIMITER ;

-- Validation for content_block_id Format
DELIMITER //

CREATE TRIGGER validate_content_block_id
BEFORE INSERT ON ContentBlock
FOR EACH ROW
BEGIN
    IF NEW.content_block_id NOT REGEXP '^block[0-9][1-9]$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: content_block_id must be in the format block[0-9][1-9]';
    END IF;
END //

DELIMITER ;



-- User Authentication

DELIMITER //

CREATE TRIGGER check_user_id_format
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
    DECLARE expected_user_id VARCHAR(50);
    DECLARE year_part CHAR(2);
    DECLARE month_part CHAR(2);

    -- Get the last 2 digits of the current year and the month in 2-digit format
    SET year_part = RIGHT(YEAR(CURDATE()), 2);
    SET month_part = LPAD(MONTH(CURDATE()), 2, '0');

    -- Concatenate to form the expected user_id based on first_name, last_name, year, and month
    SET expected_user_id = CONCAT(
        LEFT(NEW.first_name, 2),
        LEFT(NEW.last_name, 2),
        year_part,
        month_part
    );

    -- Check if the provided user_id matches the expected format
    IF NEW.user_id != expected_user_id THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: user_id must follow the format: first 2 letters of first_name + last_name + last 2 digits of year + month';
    END IF;
END //

DELIMITER ;


-- Notification Trigger

DELIMITER //

CREATE TRIGGER score_update_notification
AFTER INSERT ON Score
FOR EACH ROW
BEGIN
    INSERT INTO Notification (message, user_id, status, timestamp)
    VALUES (
        CONCAT('Score has been updated with score_id ', NEW.score_id),
        NEW.student_id,
        'unread',
        NOW()
    );
END //

CREATE TRIGGER score_change_notification
AFTER UPDATE ON Score
FOR EACH ROW
BEGIN
    INSERT INTO Notification (message, user_id, status, timestamp)
    VALUES (
        CONCAT('Score has been updated with score_id ', NEW.score_id),
        NEW.student_id,
        'unread',
        NOW()
    );
END //

DELIMITER ;


INSERT INTO User (user_id, first_name, last_name, email, password, role)
VALUES ('adad2411', 'admin', 'admin', 'admin@example.com', 'pass', 'admin');

