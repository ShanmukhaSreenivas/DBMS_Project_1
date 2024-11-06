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

