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
