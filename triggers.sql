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