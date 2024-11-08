import mysql.connector
from datetime import datetime


def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="springstudent",
        password="springstudent",
        database="proj1",
    )


def main_menu():
    while True:
        print("\nStart Menu:")
        print("1. Admin Login")
        print("2. Faculty Login")
        print("3. TA Login")
        print("4. Student Login")
        print("5. Run SQL Queries")
        print("6. Exit")

        option = input("Select an option (1-5): ")

        if option == '1':
            user_login('admin')
        elif option == '2':
            user_login('faculty')
        elif option == '3':
            user_login('ta')
        elif option == '4':
            student_login()
        elif option == '5':
            run_queries()
        elif option == '6':
            print("Exiting the application.")
            exit()
        else:
            print("Invalid option. Please enter a number between 1 and 5.")

def run_queries():
    while True:
        conn = get_db_connection()
        cursor = conn.cursor()
        print("\n\n\nQueries Menu")
        print("1. Write a query that prints the number of sections of the first chapter of a textbook.")
        print("2. Print the names of faculty and TAs of all courses. For each person print their role next to their names.")
        print("3. For each active course, print the course id, faculty member and total number of students.")
        print("4. Find the course which the largest waiting list, print the course id and the total number of people on the list")
        print("5. Print the contents of Chapter 02 of textbook 101 in proper sequence.")
        print("6. For Q2 of Activity0 in Sec02 of Chap01 in textbook 101, print the incorrect answers for that question and their corresponding explanations.")
        print("7. Find any book that is in active status by one instructor but evaluation status by a different instructor.")
        print("8. Go Back")
        
        option = input("Choose an option (1-8): ")
        
        
        if option == '1':
            query = """
            SELECT COUNT(s.section_id) FROM section s
            JOIN etextbook e ON e.textbook_id = s.textbook_id
            JOIN chapter c ON c.chapter_id = s.chapter_id
            AND c.textbook_id = s.textbook_id
            WHERE
            e.textbook_id = '101'-- 'Enter the Textbook ID here'
            AND c.chapter_id = 'chap01'; 
            """
            print("Running the query with texbook_id = 101 and chapter_id = chap01\n")
            
            cursor.execute(query)
            output = cursor.fetchall()[0][0]
            
            print(output)
        
        elif option == '2':
            query = """
            SELECT 
            t.course_id AS 'Course',
            CONCAT(u.first_name, " ", u.last_name) AS 'Name',
            u.role as 'Role'
            FROM user u
            JOIN teachingassistant t
            ON (t.faculty_id = u.user_id OR t.teaching_assistant_id = u.user_id)
            WHERE t.course_id IS NOT NULL
            ORDER BY t.course_id ASC, u.role ASC; 
            """
            print("Running the query\n")
            
            cursor.execute(query)
            output = cursor.fetchall()
            
            for out in output:
                print(out)
            
            
        elif option == '3':
            query = """
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
            """
            print("Running the query\n")
            
            cursor.execute(query)
            output = cursor.fetchall()
            
            for out in output:
                print(out)
                
        elif option == '4':
            query = """
            SELECT course_id 'Course ID', wc 'Waitlist Count'
            FROM (SELECT c1.course_id, COUNT(s1.student_id) AS 'wc'
            FROM course c1
            JOIN enrollment e1 ON e1.course_id = c1.course_id
            JOIN student s1 ON s1.student_id = e1.student_id
            WHERE e1.status = 'pending'
            GROUP BY c1.course_id
            ORDER BY COUNT(s1.student_id) DESC) wait_table
            WHERE 1=1 LIMIT 1;
            """
            print("Running the query\n")
            
            cursor.execute(query)
            output = cursor.fetchall()
            
            for out in output:
                print(out)
                
        elif option == '5':
            query = """
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
            """
            print("Running the query\n")
            
            cursor.execute(query)
            output = cursor.fetchall()
            
            for out in output:
                print(out)
        elif option == '6':
            query = """
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
            """
            print("Running the query\n")
            
            cursor.execute(query)
            output = cursor.fetchall()
            
            for out in output:
                print(out)
        elif option == '7':
            query = """
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
            """
            print("Running the query\n")
            
            cursor.execute(query)
            output = cursor.fetchall()
            
            for out in output:
                print(out)
        elif option == '8':
            cursor.close()
            conn.close()
            return main_menu()
        else:
            print("Invalid option. Please enter 1 or 8.")
            continue
        
        cursor.close()
        conn.close()


def user_login(user_type):
    while True:
        print(f"\nLogin Page for {user_type.capitalize()}")
        print("1. Sign-In")
        print("2. Go Back")

        option = input("Choose an option (1-2): ")

        if option == '1':
            user_id = input("Enter User ID: ")
            password = input("Enter Password: ")

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM User WHERE user_id=%s AND password=%s AND role=%s",
                (user_id, password, user_type),
            )
            user = cursor.fetchone()

            if user:
                print(f"Login successful. Welcome {user_type.capitalize()}!")
                if user_type == 'admin':
                    admin_home()
                elif user_type == 'faculty':
                    faculty_landing(user[0])
                elif user_type == 'ta':
                    ta_landing_page(user[0])
                elif user_type == 'student':
                    student_home()
                break
            else:
                print("Invalid credentials. Login failed.")

            cursor.close()
            conn.close()

        elif option == '2':
            print("Redirecting to the Main Menu...")
            return main_menu()

        else:
            print("Invalid option. Please enter 1 or 2.")


def admin_home():
    while True:
        print("\nAdmin Landing Menu")
        print("1. Create a Faculty Account")
        print("2. Create E-textbook")
        print("3. Modify E-textbooks")
        print("4. Create New Active Course")
        print("5. Create New Evaluation Course")
        print("6. Logout")

        option = input("Enter choice (1-6): ")

        if option == '1':
            create_faculty_account()
        elif option == '2':
            create_e_textbook()
        elif option == '3':
            modify_etextbook()
        elif option == '4':
            create_new_active_course()
        elif option == '5':
            create_new_eval_course()
        elif option == '6':
            print("Logging out. Returning to the Home page.")
            main_menu()
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


def create_faculty_account():
    while True:
        print("\nCreate a Faculty Account")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")

        user_id_prefix = first_name[:2] + last_name[:2]
        current_date = datetime.now()
        user_id_date = current_date.strftime("%y%m")
        user_id = user_id_prefix + user_id_date
        print(f"Generated User ID: {user_id}")

        print("\n1. Add User")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    print(
                        "A user with this email already exists. Please try again with a different email."
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO User (user_id, first_name, last_name, email, password, role)
                        VALUES (%s, %s, %s, %s, %s, 'faculty')
                    """,
                        (user_id, first_name, last_name, email, password),
                    )

                    cursor.execute(
                        """
                        INSERT INTO Faculty (faculty_id)
                        VALUES (%s)
                    """,
                        (user_id,),
                    )

                    conn.commit()
                    print(
                        "Faculty account created successfully in both User and Faculty tables!"
                    )
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return

        elif choice == '2':
            print("Discarding input. Returning to Admin Landing Page...")
            return
        else:
            print("Invalid choice. Please select 1 or 2.")


def create_e_textbook():
    while True:
        print("\nCreation of an E-textbook")
        title = input("Enter a new textbook title: ")
        textbook_id = input("Enter a new unique textbook ID: ")

        print("\n1. Add a new chapter to the textbook")
        print("2. Go Back")
        choice = input("Enter a choice (1-2): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "SELECT * FROM ETextbook WHERE textbook_id=%s", (textbook_id,)
                )
                existing_textbook = cursor.fetchone()

                if existing_textbook:
                    print(
                        "Entered textbook ID already exists. Please enter a new unique textbook ID."
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ETextbook (textbook_id, title)
                        VALUES (%s, %s)
                    """,
                        (textbook_id, title),
                    )
                    conn.commit()
                    print("An E-textbook was successfully added!")
                    add_new_chapter(textbook_id)
                    return
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            print("Discarding the entered input and going back to Admin Landing Page now")
            return
        else:
            print("Entered choice is Invalid. Please select 1 or 2.")


def add_new_chapter(textbook_id):
    while True:
        print(f"\nAddition of a new Chapter for the textbook: {textbook_id}")
        chapter_id = input("Enter a new Unique chapter ID: ")
        chapter_title = input("Enter a new chapter Title: ")
        print("\n1. Add a new Section")
        print("2. Go Back")
        print("3. Return to Landing Page")
        choice = input("Enter a choice (1-3): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO Chapter (chapter_id, title, textbook_id)
                    VALUES (%s, %s, %s)
                """,
                    (chapter_id, chapter_title, textbook_id),
                )
                conn.commit()
                
                print("A new chapter had been added successfully to the textbook!")
                return add_new_section(chapter_id, textbook_id)
            except mysql.connector.Error as err:
                if "chapter_id must be in the format" in str(err):
                    print(f"Error: {err}")
                    print(
                        "Entered chapter ID is invalid. Please enter a valid chapter_id with the format 'chap[0-9][1-9]'."
                    )
                else:
                    print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            print("Discarding the provided input. Returning to the previous page...")
            return create_e_textbook()

        elif choice == '3':
            print("Discarding the previous input. Returning to the Admin Landing Page...")
            return admin_home()

        else:
            print("Entered an Invalid choice. Please select (1 - 3).")


def add_new_section(chapter_id, textbook_id):
    while True:
        print(f"\nAdding a new Section to the chapter (ID: {chapter_id})")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s",
            (chapter_id, textbook_id),
        )
        chapter = cursor.fetchone()

        if not chapter:
            print(
                f"A chapter with the chapter ID {chapter_id} doesn't exist. Please enter a valid Chapter ID."
            )
            cursor.close()
            conn.close()
            break
        else:
            print(f"Chapter ID: {chapter_id} found.")
            cursor.close()
            conn.close()

        section_number = input("Enter a new Section Number: ")
        section_title = input("Enter a new Section Title: ")

        print("\n1. Add a new Content Block")
        print("2. Go Back")
        print("3. Return to Landing Page")
        choice = input("Enter a choice (1-3): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO Section (title, chapter_id, section_number, textbook_id)
                    VALUES (%s, %s, %s, %s)
                """,
                    (section_title, chapter_id, section_number, textbook_id),
                )
                conn.commit()

                cursor.execute(
                    "SELECT section_id FROM Section WHERE chapter_id = %s AND textbook_id = %s AND section_number = %s",
                    (chapter_id, textbook_id, section_number),
                )
                section_id = cursor.fetchone()[0]

                print("A new section has been added successfully!")

                return add_new_content_block(section_id)
            except mysql.connector.Error as err:
                if "section_number must be in the format" in str(err):
                    print(f"Error: {err}")
                    print(
                        "Please enter a valid section_number in the format 'sec[0-9][1-9]'."
                    )
                else:
                    print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            print("Going back to the previous page...")
            return add_new_chapter(textbook_id)

        elif choice == '3':
            print("Going back to the Admin Landing Page...")
            return admin_home()

        else:
            print("Entered an invalid choice. Please select (1-3)")


def add_new_content_block(section_id):
    while True:
        print(f"\nAddition of a new Content Block for Section (ID: {section_id})")

        content_block_id = input("Enter Unique Content Block ID:")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO ContentBlock (content_block_id, section_id) VALUES (%s, %s)",
                (
                    content_block_id,
                    section_id,
                ),
            )
            conn.commit()
            print(f"A new Content Block created with Block ID {content_block_id}.")
            print("\n1. Add some Text")
            print("2. Add a Picture")
            print("3. Add an Activity")
            print("4. Go Back")
            print("5. Return to Landing Page")

            choice = input("Enter a choice (1-5): ")
            if choice == '1':
                return add_text(content_block_id, section_id)
            elif choice == '2':
                return add_picture(content_block_id, section_id)
            elif choice == '3':
                return add_activity(content_block_id, section_id)
            elif choice == '4':
                cursor.execute(
                    "SELECT chapter_id, textbook_id FROM Section WHERE section_id = %s",
                    (section_id,),
                )
                result = cursor.fetchone()
                chapter_id, textbook_id = result
                print("Discarding entered input and going back to the previous page...")
                return add_new_section(chapter_id, textbook_id)
            elif choice == '5':
                print("Discarding entered input and going back to the User Landing Page...")
                return admin_home()
            else:
                print("Invalid choice. Please enter a choice (1-5)")
        except mysql.connector.Error as err:
            if "content_block_id must be in the format" in str(err):
                print(f"Error: {err}")
                print(
                    "Please enter a valid Content Block ID the format 'sec[0-9][1-9]'."
                )
            else:
                print(f"An error occurred: {err}")
                cursor.close()
                conn.close()
                return

        cursor.close()
        conn.close()


def add_text(content_block_id, section_id):
    while True:
        print(f"\nAddition of Text to Content Block (ID: {content_block_id})")
        text_content = input("Enter text content: ")

        print("\n1. Add")
        print("2. Go Back")
        print("3. Landing Page")

        choice = input("Enter choice (1-3): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s",
                    ('text', text_content, content_block_id, section_id),
                )
                conn.commit()
                print(
                    f"Text content added to Content Block {content_block_id} successfully!"
                )
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

            return add_new_content_block(section_id)

        elif choice == '2':
            print("Discarding current input and going back to the previous page...")
            return add_new_content_block(section_id)

        elif choice == '3':
            print("Discarding current input and going back to the User Landing Page...")
            return admin_home()

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def add_picture(content_block_id, section_id):
    while True:
        print(f"\nAddition of a Picture to Content Block (ID: {content_block_id})")
        picture_url = input("Enter picture URL: ")

        print("\n1. Add")
        print("2. Go Back")
        print("3. Return to the Landing Page")

        choice = input("Enter a choice (1-3): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s",
                    ('picture', picture_url, content_block_id, section_id),
                )
                conn.commit()
                print(
                    f"A picture URL has been added to Content Block {content_block_id} successfully!"
                )
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

            return add_new_content_block(section_id)

        elif choice == '2':
            print("Discarding entered input and returning to the previous page")
            return add_new_content_block(section_id)

        elif choice == '3':
            print("Discarding entered input and Returning to the User Landing Page")
            return admin_home()

        else:
            print("Entered an Invalid choice. Please select (1-3).")


def add_activity(content_block_id, section_id):
    while True:
        print(f"\nAddition of an activity to Content Block (ID: {content_block_id})")
        activity_id = input("Enter a new Unique Activity ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO Activity (activity_id, content_block_id, section_id)
                VALUES (%s, %s, %s)
            """,
                (
                    activity_id,
                    content_block_id,
                    section_id,
                ),
            )
            conn.commit()
            print(
                f"Activity with an ID {activity_id} added successfully to Content Block {content_block_id}."
            )
        except mysql.connector.Error as err:
            print(f"Failure. An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add a new Question")
        print("2. Go Back")
        print("3. Return to Landing Page")

        choice = input("Enter a choice (1-3): ")

        if choice == '1':
            add_question(activity_id, content_block_id, section_id)
            return

        elif choice == '2':
            print("Discarding current input and going back to the previous page...")
            return add_new_content_block(section_id)

        elif choice == '3':
            print("Discarding current input and going back to the User Landing Page...")
            return admin_home()

        else:
            print("Entered an Invalid choice. Please select (1-3).")


def add_question(activity_id, content_block_id, section_id):
    while True:
        print("\nAddition of a new Question")

        question_id = input("Enter a new Question ID: ")
        question_text = input("Enter new Question Text: ")

        option1_text = input("Enter the Option 1 Text: ")
        option1_explanation = input("Enter the Option 1 Explanation: ")

        option2_text = input("Enter the Option 2 Text: ")
        option2_explanation = input("Enter the Option 2 Explanation: ")

        option3_text = input("Enter the Option 3 Text: ")
        option3_explanation = input("Enter the Option 3 Explanation: ")

        option4_text = input("Enter the Option 4 Text: ")
        option4_explanation = input("Enter the Option 4 Explanation: ")

        correct_option = input("Enter the correct answer, ranging from (1-4): ")

        print("\n1. Save")
        print("2. Cancel")
        print("3. Return to Landing Page")
        choice = input("Enter a choice (1-3): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO Question (question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option, activity_id, section_id, content_block_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        question_id,
                        question_text,
                        option1_text,
                        option2_text,
                        option3_text,
                        option4_text,
                        option1_explanation,
                        option2_explanation,
                        option3_explanation,
                        option4_explanation,
                        correct_option,
                        activity_id,
                        section_id,
                        content_block_id,
                    ),
                )
                conn.commit()
                print("Entered Question and options were added successfully!")
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return add_activity(content_block_id, section_id)

        elif choice == '2':
            print("Discarding current input and returning to Add Activity page...")
            return add_activity(content_block_id, section_id)

        elif choice == '3':
            print("Discarding current input and Returning to Admin Landing Page...")
            return

        else:
            print("Entered an Invalid choice. Please select (1-3)).")


def add_question_faculty(activity_id, content_block_id, section_id, faculty_id):
    while True:
        print("\nAddition of a Question for faculty")

        question_id = input("Enter a new Question ID: ")
        question_text = input("Enter new Question Text: ")

        option1_text = input("Enter the Option 1 Text: ")
        option1_explanation = input("Enter the Option 1 Explanation: ")

        option2_text = input("Enter the Option 2 Text: ")
        option2_explanation = input("Enter the Option 2 Explanation: ")

        option3_text = input("Enter the Option 3 Text: ")
        option3_explanation = input("Enter the Option 3 Explanation: ")

        option4_text = input("Enter the Option 4 Text: ")
        option4_explanation = input("Enter the Option 4 Explanation: ")

        correct_option = input("Enter the correct answer option (1-4): ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter a choice (1-2): ")

        if choice == '1':
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO Question (question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option, activity_id, section_id, content_block_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        question_id,
                        question_text,
                        option1_text,
                        option2_text,
                        option3_text,
                        option4_text,
                        option1_explanation,
                        option2_explanation,
                        option3_explanation,
                        option4_explanation,
                        correct_option,
                        activity_id,
                        section_id,
                        content_block_id,
                    ),
                )
                conn.commit()
                print("Question and options were added successfully!")
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return add_activity_faculty(content_block_id, section_id, faculty_id)

        elif choice == '2':
            print("Discarding the entered input and returning to the Addition Activity page...")
            return add_activity_faculty(content_block_id, section_id, faculty_id)
        else:
            print("Entered an Invalid choice. Please select (1-2).")


def modify_etextbook():
    while True:
        print("\nModification of an E-textbook")
        textbook_id = input("Enter a Unique E-textbook ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ETextbook WHERE textbook_id = %s", (textbook_id,))
        textbook = cursor.fetchone()

        if not textbook:
            print(
                f"Textbook with the ID {textbook_id} is non-existent in the db. Please enter a valid ID."
            )
            cursor.close()
            conn.close()
            continue
        else:
            print(f"Textbook with Textbook ID {textbook_id} was found")
            cursor.close()
            conn.close()

        print("\n1. Add New Chapter")
        print("2. Modify Chapter")
        print("3. Go Back")
        print("4. Return to the Landing Page")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            add_new_chapter(textbook_id)
            return modify_etextbook()

        elif choice == '2':
            modify_chapter(textbook_id)
            return modify_etextbook()

        elif choice == '3':
            print("Going back to the previous page")
            return

        elif choice == '4':
            print("Going back to the Admin Landing Page")
            return

        else:
            print("Entered an Invalid choice. Please select (1-4)")


def modify_chapter(textbook_id):
    while True:
        print(f"\nModification of a Chapter for Textbook ID: {textbook_id}")
        chapter_id = input("Enter an existing Unique Chapter ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s",
            (chapter_id, textbook_id),
        )
        chapter = cursor.fetchone()

        if not chapter:
            print(
                f"Chapter with ID {chapter_id} does not exist for the Textbook ID {textbook_id}. Please enter a valid Chapter ID."
            )
            cursor.close()
            conn.close()
            break
        else:
            print(f"Chapter with ID {chapter_id} found.")
            cursor.close()
            conn.close()

        print("\n1. Add New Section")
        print("2. Modify Section")
        print("3. Go Back")
        print("4. Return to the Landing Page")
        choice = input("Enter a choice (1-4): ")

        if choice == '1':
            add_new_section(chapter_id, textbook_id)
            return modify_chapter(textbook_id)

        elif choice == '2':
            modify_section(chapter_id, textbook_id)
            return modify_chapter(textbook_id)

        elif choice == '3':
            print("Going back to the previous page")
            return

        elif choice == '4':
            print("Going back to the Admin Landing Page...")
            return

        else:
            print("Entered an Invalid choice. Please select (1-4).")


def modify_section(chapter_id, textbook_id):
    while True:
        print("\nModification of a Section")

        section_num = input("Enter an existing Section Number: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                SELECT section_id FROM Section
                WHERE section_number = %s AND chapter_id = %s AND textbook_id = %s
            """,
                (section_num, chapter_id, textbook_id),
            )

            section_id = cursor.fetchone()[0]

            if not section_id:
                print(
                    "Section was not found for the given E-textbook ID, Chapter ID, and Section number. Please try again."
                )
                continue
            else:
                print("Section found successfully!")

                print("\n1. Add New Content Block")
                print("2. Modify Content Block")
                print("3. Go Back")
                print("4. Return to Landing Page")

                choice = input("Enter choice (1-4): ")

                if choice == '1':
                    add_new_content_block(section_id)
                    return modify_section(chapter_id, textbook_id)

                elif choice == '2':
                    modify_content_block(section_id)
                    return modify_section(chapter_id, textbook_id)

                elif choice == '3':
                    print("Going back to the previous page")
                    return

                elif choice == '4':
                    print("Going back to the Admin Landing Page")
                    return

                else:
                    print("Invalid choice. Please select a number between 1 and 4.")
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()


def modify_content_block(section_id):
    while True:
        print("\n Modify Content Block ")
        content_block_id = input("Enter Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                "SELECT * FROM ContentBlock WHERE content_block_id = %s",
                (content_block_id,),
            )
            content_block = cursor.fetchone()

            if not content_block:
                print("Content Block not found for the given ID. Please try again.")
            else:
                print("Content Block found successfully!")

                print("\n1. Add Text")
                print("2. Add Picture")
                print("3. Add New Activity")
                print("4. Go Back")
                print("5. Return to Landing Page")

                choice = input("Enter a choice (1-5): ")

                if choice == '1':
                    add_text(content_block_id, section_id)
                    return modify_content_block(section_id)

                elif choice == '2':
                    add_picture(content_block_id, section_id)
                    return modify_content_block(section_id)

                elif choice == '3':
                    add_activity(content_block_id)
                    return modify_content_block(section_id)

                elif choice == '4':
                    print("Returning to the previous page")
                    return

                elif choice == '5':
                    print("Returning to the Admin Landing Page")
                    return

                else:
                    print("Entered an Invalid choice. Please select a number between (1-5).")
        except mysql.connector.Error as err:
            print(f"Failure. An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()


def create_new_active_course():
    while True:
        print("\nCreation of a Active Course")
        course_id = input("Enter a Unique Course ID: ")
        course_title = input("Enter a Course Name: ")
        textbook_id = input("Enter a Unique ID of the E-textbook: ")
        faculty_id = input("Enter a Faculty Member ID: ")
        start_date = input("Enter a Course Start Date (YYYY-MM-DD): ")
        end_date = input("Enter a Course End Date (YYYY-MM-DD): ")
        course_token = input("Enter a Unique Token: ")
        capacity = input("Enter a Course Capacity: ")

        print("\n1. Save")
        print("2. Cancel")
        print("3. Return to Landing Page")

        choice = input("Enter choice (1-3): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Course WHERE course_id = %s", (course_id,)
                )
                existing_course = cursor.fetchone()

                if existing_course:
                    print(
                        "A course with this ID already exists. Please try again with a different ID."
                    )
                    continue

                cursor.execute(
                    "SELECT * FROM ETextbook WHERE textbook_id = %s", (textbook_id,)
                )
                textbook = cursor.fetchone()

                if not textbook:
                    print(
                        "The provided E-textbook ID does not exist. Please enter a valid E-textbook ID."
                    )
                    continue

                cursor.execute(
                    "SELECT * FROM User WHERE user_id = %s AND role = 'faculty'",
                    (faculty_id,),
                )
                faculty = cursor.fetchone()

                if not faculty:
                    print(
                        "The provided Faculty Member ID does not exist or is not assigned to a faculty. Please enter a valid Faculty ID."
                    )
                    continue

                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                cursor.execute(
                    """
                    INSERT INTO Course (course_id, title, faculty_id, start_date, end_date, course_type, course_token, capacity, textbook_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        course_id,
                        course_title,
                        faculty_id,
                        start_date,
                        end_date,
                        'active',
                        course_token,
                        capacity,
                        textbook_id,
                    ),
                )

                conn.commit()

                print("New Active Course created successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")

            finally:
                cursor.close()
                conn.close()

            return

        elif choice == '2':
            print("Discarding current input and returning to the Admin Landing Page")
            return

        elif choice == '3':
            print("Going back to the Admin Landing Page...")
            return

        else:
            print("Entered an Invalid choice. Please select (1-3).")


def create_new_eval_course():
    while True:
        print("\nCreate New Evaluation Course")
        course_id = input("Enter a Unique Course ID: ")
        course_title = input("Enter a Course Name: ")  
        
        
        
        textbook_id = input("Enter a Unique ID of the E-textbook: ")
        faculty_id = input("Enter a Faculty Member ID: ")
        start_date = input("Enter a Course Start Date (YYYY-MM-DD): ")
        
        
        end_date = input("Enter a Course End Date (YYYY-MM-DD): ")
        token = input("Enter a Unique Token: ")
        capacity = input("Enter a Course Capacity: ")

        print("\n1. Save")
        print("2. Cancel")
        print("3. Return to the Landing Page")
        choice = input("Enter choice (1-3): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Course WHERE course_id = %s", (course_id,)
                )
                existing_course = cursor.fetchone()

                if existing_course:
                    print(
                        "A course with this ID already exists. Please try again with a different ID."
                    )
                    continue

                cursor.execute(
                    "SELECT * FROM ETextbook WHERE textbook_id = %s", (textbook_id,)
                )
                textbook = cursor.fetchone()

                if not textbook:
                    print(
                        "The provided E-textbook ID does not exist. Please enter a valid E-textbook ID."
                    )
                    continue

                cursor.execute(
                    "SELECT * FROM User WHERE user_id = %s AND role = 'faculty'",
                    (faculty_id,),
                )
                faculty = cursor.fetchone()

                if not faculty:
                    print(
                        "The provided Faculty Member ID does not exist or is not assigned to a faculty. Please enter a valid Faculty ID."
                    )
                    continue

                cursor.execute(
                    """
                    INSERT INTO Course (course_id, title, faculty_id, start_date, end_date, course_type, course_token, capacity, textbook_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        course_id,
                        course_title,
                        faculty_id,
                        start_date,
                        end_date,
                        'evaluation',
                        token,
                        capacity,
                        textbook_id,
                    ),
                )
                conn.commit()

                print("New Evaluation Course created successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return

        elif choice == '2':
            print("Discarding entered input and returning to the Admin Landing Page")
            return

        elif choice == '3':
            print("Going back to the Admin Landing Page")
            return

        else:
            print("Entered an Invalid choice. Please select (1-3).")


def faculty_login():
    while True:
        print("\nFaculty Login")
        print("1. Sign-In")
        print("2. Go Back")

        choice = input("Choose an option (1-2): ")

        if choice == '1':

            user_id = input("Enter your User ID: ")
            password = input("Enter your Password: ")

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "SELECT * FROM User WHERE user_id = %s AND password = %s AND role = 'faculty'",
                    (user_id, password),
                )
                user = cursor.fetchone()

                if user:
                    print("Login was successful. Welcome Faculty!")
                    faculty_landing(user_id)
                    break
                else:
                    print("Login was Incorrect. Please try again.")

            except mysql.connector.Error as err:
                print(f"Failure.An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()





        elif choice == '2':

            print("Returning to the Home page...")
            main_menu()
            break

        else:
            print("Entered an Invalid choice. Please enter (1-2).")


def faculty_landing(faculty_id):
    while True:
        print("Faculty Home: Welcome!")
        print("\nFaculty Landing Menu")
        print("1. Go to Active Course")
        print("2. Go to Evaluation Course")
        print("3. View Courses")
        print("4. Change Password")
        print("5. Logout")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            go_to_active_course(faculty_id)
        elif choice == '2':
            go_to_evaluation_course(faculty_id)
        elif choice == '3':
            view_courses(faculty_id)
        elif choice == '4':
            change_password(faculty_id)
        elif choice == '5':
            print("Logging out and going back to the Home page.")
            main_menu()
            break
        else:
            print("Entered an Invalid choice. Please enter a choice between (1-5).")


def go_to_active_course(faculty_id):
    while True:
        course_id = input("Enter a Active Course ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Course WHERE course_type = 'active' AND faculty_id = %s AND course_id = %s",
            (
                faculty_id,
                course_id,
            ),
        )
        active_course = cursor.fetchone()

        if not active_course:
            print("Entered an Invalid Course ID. Please try again.")
            cursor.close()
            conn.close()
            continue
        else:
            cursor.execute(
                "SELECT textbook_id FROM Course WHERE course_id = %s", (course_id,)
            )
            textbook_id = cursor.fetchone()[0]

            print(f"\nActive Course Functions for the Course ID: {course_id}")
            print("1. View Worklist")
            print("2. Approve Enrollment")
            print("3. View Students")
            print("4. Add New Chapter")
            print("5. Modify Chapters")
            print("6. Add TA")
            print("7. Go Back")

            choice = input("Enter a choice (1-7): ")

            if choice == '1':
                view_worklist(faculty_id)
            elif choice == '2':
                approve_enrollment(faculty_id)
            elif choice == '3':
                view_students(faculty_id)
            elif choice == '4':
                add_new_chapter_faculty(textbook_id, faculty_id)
            elif choice == '5':
                modify_chapter_faculty(textbook_id, faculty_id)
            elif choice == '6':
                add_ta(faculty_id)
            elif choice == '7':
                print("Going back to Faculty Landing Page")
                faculty_landing(faculty_id)
                break
            else:
                print("Entered an Invalid choice. Please enter a choice (1-7).")

        cursor.close()
        conn.close()


def view_worklist(faculty_id):
    while True:
        try:
            print("\nView Worklist Functionality")

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT u.user_id, u.first_name, u.last_name, c.title
                FROM User u
                JOIN Enrollment e ON u.user_id = e.student_id
                JOIN Course c ON e.course_id = c.course_id
                WHERE c.faculty_id = %s AND e.status = 'pending' AND u.role = 'student'
            """,
                (faculty_id,),
            )

            worklist = cursor.fetchall()

            if worklist:
                print("\nCurrent Students in Waiting List")
                for student in worklist:
                    print(
                        f"Student ID: {student[0]}, Name: {student[1]} {student[2]}, Course: {student[3]}"
                    )
            else:
                print("The waitlist is currently empty")

            print("\n1. Go back")
            choice = input("Enter a choice (1 to Go Back): ")

            if choice == '1':
                print("Going back to the Faculty: Active Course page")
                go_to_active_course(faculty_id)
                break
            else:
                print("Entered an Invalid choice. Please select 1 to Go Back.")
        except Exception as msg:
            print(f"Failure. An error occurred: {msg}")
            return faculty_landing(faculty_id)
        except mysql.connector.Error as err:
            print(f"Failure. An error occurred: {err}")
            return faculty_landing(faculty_id)
        finally:
            cursor.close()
            conn.close()


def approve_enrollment(faculty_id):
    while True:
        print("\nApprove Student Enrollment")

        student_id = input("Enter the Student ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT e.enrollment_id, c.title
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            WHERE e.student_id = %s AND c.faculty_id = %s AND e.status = 'pending'
        """,
            (student_id, faculty_id),
        )

        enrollment_record = cursor.fetchone()

        if enrollment_record:
            enrollment_id = enrollment_record[0]
            course_name = enrollment_record[1]
            print(
                f"Student ID {student_id} is waiting for approval in the course: {course_name}"
            )

            print("\n1. Save (to Approve Student Enrollment)")
            print("2. Cancel")

            choice = input("Enter choice (1-2): ")

            if choice == '1':
                try:

                    cursor.execute(
                        """
                        UPDATE Enrollment
                        SET status = 'approved'
                        WHERE enrollment_id = %s
                    """,
                        (enrollment_id,),
                    )
                    conn.commit()
                    print(
                        f"Enrollment for Student ID {student_id} in course {course_name} has been approved."
                    )
                except mysql.connector.Error as err:
                    print(f"Failure. An error occurred: {err}")
                finally:
                    cursor.close()
                    conn.close()
                return

            elif choice == '2':
                print("Discarding enrollment approval input. Going back to the previous page.")
                cursor.close()
                conn.close()
                return
            else:
                print("Entered an Invalid choice. Please select (1-2).")
        else:
            print(
                f"No pending enrollment found for Student ID {student_id}. Please try again."
            )
            cursor.close()
            conn.close()


def view_students(faculty_id):
    while True:
        print("\nView Students")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT c.course_id, c.title
            FROM Course c
            WHERE c.faculty_id = %s
        """,
            (faculty_id,),
        )
        courses = cursor.fetchall()

        if courses:
            print("\nCourses that are supervised by you:")
            for idx, course in enumerate(courses, 1):
                print(f"{idx}. {course[1]} (ID: {course[0]})")

            try:

                cursor.execute(
                    """
                    SELECT DISTINCT s.user_id, s.first_name, s.last_name, e.course_id
                    FROM User s
                    JOIN Enrollment e ON s.user_id = e.student_id
                    WHERE e.course_id IN (
                                SELECT c.course_id
                                FROM Course c
                                WHERE c.faculty_id = %s
                                AND c.course_type = 'active'
                               ) AND e.status = 'approved'
                    ORDER BY e.course_id ASC, s.user_id ASC
                """,
                    (faculty_id,),
                )
                students = cursor.fetchall()

                if students:
                    print(f"\nStudents  currently enrolled:")
                    for student in students:
                        print(
                            f"Course ID: {student[3]}, ID: {student[0]}, Name: {student[1]} {student[2]}"
                        )
                else:
                    print(f"\nNo students found for the course")

            except ValueError:
                print("Entered an Invalid input. Please enter a number.")

        else:
            print("No courses are supervised by you")

        cursor.close()
        conn.close()

        print("\n1. Go Back")
        choice = input("Enter choice (1 to Go Back): ")

        if choice == '1':
            print("Going back to the previous page.")
            break
        else:
            print("Invalid choice. Please enter 1 to go back.")


from datetime import datetime


def add_ta(faculty_id):
    while True:
        print("\nAddition of a Teaching Assistant (TA)")

        first_name = input("Enter the TA's First Name: ")
        last_name = input("Enter the TA's Last Name: ")
        email = input("Enter the TA's Email: ")
        default_password = input("Enter a Default Password: ")

        user_id_prefix = first_name[:2].upper() + last_name[:2].upper()
        current_date = datetime.now()
        user_id_date = current_date.strftime("%y%m")
        user_id = user_id_prefix + user_id_date
        print(user_id)

        print("\n1. Save")
        print("2. Cancel")

        choice = input("Enter a choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    print(
                        "User email already exists in the system. Please try again with a different email."
                    )
                else:

                    cursor.execute(
                        """
                        INSERT INTO User (user_id, first_name, last_name, email, password, role)
                        VALUES (%s, %s, %s, %s, %s, 'ta')
                    """,
                        (user_id, first_name, last_name, email, default_password),
                    )
                    conn.commit()
                    print("Teaching Assistant was added successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")

            finally:
                cursor.close()
                conn.close()

            return

        elif choice == '2':

            print("Discarding input and going back to the previous page.")
            return

        else:
            print("Entered an Invalid choice. Please select (1-2).")


def add_new_chapter_faculty(textbook_id, faculty_id):
    while True:
        print("\nAdd New Chapter")

        chapter_id = input("Enter a Unique Chapter ID: ")
        chapter_title = input("Enter Chapter Title: ")
        print("\n1. Add New Section")
        print("2. Go Back")

        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Chapter WHERE chapter_id=%s", (chapter_id,)
                )
                existing_chapter = cursor.fetchone()

                if existing_chapter:
                    print(
                        "Use a different CHapter ID as one already exists with this ID."
                    )
                    return add_new_chapter_faculty(textbook_id)
                else:

                    cursor.execute(
                        """
                    INSERT INTO Chapter (chapter_id, title, textbook_id)
                    VALUES (%s, %s, %s)
                """,
                        (chapter_id, chapter_title, textbook_id),
                    )
                    conn.commit()
                    print("Chapter added successfully!")
                    return add_new_section_faculty(chapter_id, textbook_id, faculty_id)

            except mysql.connector.Error as err:
                if "chapter_id must be in the format" in str(err):
                    print(f"Error: {err}")
                    print(
                        "Please enter a valid chapter_id in the format 'chap[0-9][1-9]'."
                    )
                else:
                    print(f"Failure. An error occurred: {err}")

            finally:
                cursor.close()
                conn.close()

            return

        elif choice == '2':

            print("Discarding input and going back to the previous page.")
            return faculty_landing(faculty_id)

        else:
            print("Invalid choice. Please select (1-2).")


def modify_chapter_faculty(textbook_id, faculty_id):
    while True:
        print("\nModification of Chapter")

        chapter_id = input("Enter Unique Chapter ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s",
            (chapter_id, textbook_id),
        )
        chapter = cursor.fetchone()

        if not chapter:
            print("The chapter ID does not exist. Please enter a valid Chapter ID.")
            cursor.close()
            conn.close()
            continue

        print("\n1. Hide Chapter")
        print("2. Delete Chapter")
        print("3. Add New Section")
        print("4. Modify Section")
        print("5. Go Back")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            hide_chapter(chapter_id, textbook_id)
        elif choice == '2':
            delete_chapter(chapter_id, textbook_id)
        elif choice == '3':
            add_new_section_faculty(chapter_id, textbook_id, faculty_id)
        elif choice == '4':
            modify_section_faculty(chapter_id, textbook_id, faculty_id)
        elif choice == '5':
            print("Going back to the previous page")
            break
        else:
            print("Entered an Invalid choice. Please select a number between (1-5).")

        cursor.close()
        conn.close()


def hide_chapter(chapter_id, textbook_id):
    while True:
        print("\nHide Chapter")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('hide_chapter', [chapter_id, textbook_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
            except mysql.connector.Error as err:
                print(f"Failed: An error occurred - {err}")
            finally:
                cursor.close()
                conn.close()
            break
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def delete_chapter(chapter_id, textbook_id):
    while True:
        print("\nDelete Chapter")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('delete_chapter', [chapter_id, textbook_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
            except mysql.connector.Error as err:
                print(f"Failed: An error occurred - {err}")
            finally:
                cursor.close()
                conn.close()
            break
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def add_new_section_faculty(chapter_id, textbook_id, faculty_id):
    while True:
        print("\nAdd New Section")
        section_number = input("Enter Section Number: ")
        section_title = input("Enter Section Title: ")

        print("\n1. Add New Content Block")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Section WHERE section_number=%s AND chapter_id=%s AND textbook_id = %s",
                    (section_number, chapter_id, textbook_id),
                )
                existing_section = cursor.fetchone()

                if existing_section:
                    print(
                        f"A section with number {section_number} already exists for this chapter."
                    )
                    return add_new_section_faculty(chapter_id, textbook_id, faculty_id)
                else:

                    cursor.execute(
                        """
                        INSERT INTO Section (section_number, title, chapter_id,textbook_id)
                        VALUES (%s, %s, %s, %s)
                    """,
                        (section_number, section_title, chapter_id, textbook_id),
                    )
                    conn.commit()
                    print(
                        "Section created successfully! Redirecting to Add New Content Block..."
                    )
                    cursor.execute(
                        "SELECT section_id FROM Section WHERE chapter_id = %s AND textbook_id = %s AND section_number = %s",
                        (chapter_id, textbook_id, section_number),
                    )
                    section_id = cursor.fetchone()[0]
                    return add_new_content_block_faculty(section_id, faculty_id)
            except mysql.connector.Error as err:
                if "section_number must be in the format" in str(err):
                    print(f"Error: {err}")
                    print(
                        "Please enter a valid section_number in the format 'sec[0-9][1-9]'."
                    )
                else:
                    print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input. Returning to the previous page...")
            return add_new_chapter_faculty(textbook_id, faculty_id)
        else:
            print("Invalid choice. Please select 1 or 2.")


def modify_section_faculty(chapter_id, textbook_id, faculty_id):
    while True:
        print("\nModify Section")
        section_number = input("Enter Section Number: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT section_id FROM Section
                WHERE section_number = %s AND chapter_id = %s AND textbook_id = %s
            """,
                (section_number, chapter_id, textbook_id),
            )

            section_id = cursor.fetchone()[0]

            if not section_id:
                print(f"Section {section_number} does not exist. Please try again.")
                cursor.close()
                conn.close()
                return

            print("\n1. Hide Section")
            print("2. Delete Section")
            print("3. Add New Content Block")
            print("4. Modify Content Block")
            print("5. Go Back")

            choice = input("Enter choice (1-5): ")

            if choice == '1':
                hide_section(section_id)
            elif choice == '2':
                delete_section(section_id)
            elif choice == '3':
                add_new_content_block_faculty(section_id, faculty_id)
            elif choice == '4':
                modify_content_block_faculty(section_id, faculty_id)
            elif choice == '5':
                print("Returning to the previous page...")
                break
            else:
                print("Invalid choice. Please select a valid option from 1 to 5.")
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()


def hide_section(section_id):
    while True:
        print("\nHide Section")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('hide_section', [section_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            break
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def delete_section(section_id):
    while True:
        print("\nDelete Section")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('delete_section', [section_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            break
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def add_new_content_block_faculty(section_id, faculty_id):
    while True:
        print(f"\nAdd New Content Block for Section (ID: {section_id})")

        content_block_id = input("Enter Unique Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO ContentBlock (content_block_id, section_id) VALUES (%s, %s)",
                (
                    content_block_id,
                    section_id,
                ),
            )
            conn.commit()
        except mysql.connector.Error as err:
            if "content_block_id must be in the format" in str(err):
                print(f"Error: {err}")
                print(
                    "Please enter a valid Content Block ID the format 'sec[0-9][1-9]'."
                )
            else:
                print(f"An error occurred: {err}")
            cursor.close()
            conn.close()
            return

        print("\n1. Add Text")
        print("2. Add Picture")
        print("3. Add Activity")
        print("4. Go Back")

        choice = input("Enter choice (1-4): ")

        if choice == '1':
            return add_text_faculty(content_block_id, section_id, faculty_id)

        elif choice == '2':
            return add_picture_faculty(content_block_id, section_id, faculty_id)

        elif choice == '3':
            return add_activity_faculty(content_block_id, section_id, faculty_id)

        elif choice == '4':

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT chapter_id, textbook_id FROM Section WHERE section_id = %s",
                (section_id,),
            )
            result = cursor.fetchone()
            chapter_id, textbook_id = result
            print("Going back to the previous page...")
            return add_new_section_faculty(chapter_id, textbook_id, faculty_id)
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


def modify_content_block_faculty(section_id, faculty_id):
    while True:
        print("\nModify Content Block")

        content_block_id = input("Enter Content Block ID: ")

        print("\n1. Hide Content Block")
        print("2. Delete Content Block")
        print("3. Add Text")
        print("4. Add Picture")
        print("5. Hide Activity")
        print("6. Delete Activity")
        print("7. Add Activity")
        print("8. Go Back")

        choice = input("Enter choice (1-8): ")

        if choice == '1':
            hide_content_block_faculty(section_id, content_block_id)
            return

        elif choice == '2':
            delete_content_block_faculty(section_id, content_block_id)
            return

        elif choice == '3':
            add_text_faculty(content_block_id, section_id, faculty_id)
            return

        elif choice == '4':
            add_picture_faculty(content_block_id, section_id, faculty_id)
            return

        elif choice == '5':
            hide_activity_faculty(section_id, content_block_id)
            return

        elif choice == '6':
            delete_activity_faculty(section_id, content_block_id)
            return

        elif choice == '7':
            add_activity_faculty(content_block_id, section_id, faculty_id)
            return

        elif choice == '8':

            print("Going back to the previous page...")
            return

        else:
            print("Invalid choice. Please select a number between 1 and 8.")


def hide_content_block_faculty(section_id, content_block_id):
    while True:
        print("\nHide Content Block")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    UPDATE ContentBlock
                    SET hidden = 'yes'
                    WHERE content_block_id = %s
                    AND section_id = %s
                """,
                    (content_block_id, section_id),
                )
                conn.commit()
                print("Content Block hidden successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return
        else:
            print("Invalid choice. Please select 1 or 2.")


def delete_content_block_faculty(section_id, content_block_id):
    while True:
        print("\nDelete Content Block")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "DELETE FROM ContentBlock WHERE content_block_id = %s AND section_id=%s",
                    (content_block_id, section_id),
                )
                conn.commit()
                print("Content Block deleted successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def hide_activity_faculty(section_id, content_block_id):
    while True:
        print("\nHide Activity")

        activity_id = input("Enter the unique Activity ID: ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Activity WHERE activity_id=%s AND section_id = %s AND content_block_id = %s",
                    (
                        activity_id,
                        section_id,
                        content_block_id,
                    ),
                )
                activity = cursor.fetchone()

                if activity:

                    cursor.execute(
                        """
                        UPDATE Activity
                        SET hidden = 'yes'
                        WHERE activity_id = %s AND section_id = %s AND content_block_id = %s
                    """,
                        (activity_id, section_id, content_block_id),
                    )
                    conn.commit()
                    print("Activity hidden successfully!")
                else:
                    print(f"No activity found with ID: {activity_id}")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def delete_activity_faculty(section_id, content_block_id):
    while True:
        print("\nDelete Activity")

        activity_id = input("Enter the unique Activity ID: ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Activity WHERE activity_id=%s AND section_id = %s AND content_block_id = %s",
                    (
                        activity_id,
                        section_id,
                        content_block_id,
                    ),
                )
                activity = cursor.fetchone()

                if activity:

                    cursor.execute(
                        "DELETE FROM Activity WHERE activity_id = %s AND section_id = %s AND content_block_id = %s",
                        (
                            activity_id,
                            section_id,
                            content_block_id,
                        ),
                    )
                    conn.commit()
                    print("Activity deleted successfully!")
                else:
                    print(f"No activity found with ID: {activity_id}")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def add_text_faculty(content_block_id, section_id, faculty_id):
    while True:
        print("\n Add Text to Content Block")

        text_content = input("Enter the text: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s",
                    ('text', text_content, content_block_id, section_id),
                )
                conn.commit()
                print(
                    f"Text content added to Content Block {content_block_id} successfully!"
                )

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return add_new_content_block_faculty(section_id, faculty_id)

        else:
            print("Invalid choice. Please select 1 or 2.")


def add_picture_faculty(content_block_id, section_id, faculty_id):
    while True:
        print("\nAdd Picture to Content Block")

        picture_content = input("Enter the picture file path or URL: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s",
                    ('picture', picture_content, content_block_id, section_id),
                )
                conn.commit()
                print("Picture added successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return add_new_content_block_faculty(section_id, faculty_id)

        else:
            print("Invalid choice. Please select 1 or 2.")


def add_activity_faculty(content_block_id, section_id, faculty_id):
    while True:
        print("\nAdd Activity")

        activity_id = input("Enter Unique Activity ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO Activity (activity_id, content_block_id, section_id)
                VALUES (%s, %s, %s)
            """,
                (
                    activity_id,
                    content_block_id,
                    section_id,
                ),
            )
            conn.commit()
            print(
                f"Activity with ID {activity_id} added successfully to Content Block {content_block_id}."
            )
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add Question")
        print("2. Go Back")

        choice = input("Enter choice (1-2): ")

        if choice == '1':
            add_question_faculty(activity_id, content_block_id, section_id, faculty_id)
            return

        elif choice == '2':
            print("Discarding input. Returning to the previous page...")
            return add_new_content_block_faculty(section_id, faculty_id)

        else:
            print("Invalid choice. Please select 1 or 2")


def go_to_evaluation_course(faculty_id):
    while True:
        course_id = input("Enter the Evaluation Course ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Course WHERE course_type = 'evaluation' AND faculty_id = faculty_id AND course_id = %s",
            (course_id,),
        )
        evaluation_course = cursor.fetchone()

        if not evaluation_course:
            print("Invalid Course ID. Please try again.")
            cursor.close()
            conn.close()
            continue
        else:

            cursor.execute(
                "SELECT textbook_id FROM Course WHERE course_id = %s", (course_id,)
            )
            textbook_id = cursor.fetchone()[0]
            print(f"\nEvaluation Course Menu (Course ID: {course_id})")
            print("1. Add New Chapter")
            print("2. Modify Chapters")
            print("3. Go Back")

            choice = input("Enter choice (1-3): ")

            if choice == '1':
                add_new_chapter_faculty(textbook_id, faculty_id)
            elif choice == '2':
                modify_chapter_faculty(textbook_id, faculty_id)
            elif choice == '3':
                print("Returning to Faculty Landing Page...")
                faculty_landing(faculty_id)
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

        cursor.close()
        conn.close()


def view_courses(faculty_id):
    while True:
        print(f"\nAssigned Courses for Faculty ID: {faculty_id}")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT course_id, title FROM Course WHERE faculty_id = %s", (faculty_id,)
        )
        assigned_courses = cursor.fetchall()

        if not assigned_courses:
            print("No courses assigned.")
        else:
            print("Assigned Courses:")
            for course in assigned_courses:
                print(f"Course ID: {course[0]}, Course Name: {course[1]}")

        print("\n1. Go Back")
        choice = input("Enter choice (1 to Go Back): ")

        if choice == '1':
            print("Returning to Faculty Landing Page...")
            faculty_landing(faculty_id)
            break
        else:
            print("Invalid choice. Please select 1 to go back.")

        cursor.close()
        conn.close()


def change_password(faculty_id):
    while True:
        print("\nChange Password")

        current_password = input("Enter Current Password: ")
        new_password = input("Enter New Password: ")
        confirm_password = input("Confirm New Password: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM User WHERE user_id = %s AND role = 'faculty'",
            (faculty_id,),
        )
        result = cursor.fetchone()

        if result:
            db_password = result[0]
            if db_password != current_password:
                print("Current password is incorrect. Please try again.")
            elif new_password != confirm_password:
                print("New passwords do not match. Please try again.")
            else:

                cursor.execute(
                    "UPDATE User SET password = %s WHERE user_id = %s AND role = 'faculty'",
                    (new_password, faculty_id),
                )
                conn.commit()
                print("Password updated successfully!")
                break
        else:
            print("User not found or password mismatch.")

        cursor.close()
        conn.close()

        print("\n1. Update Again")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            continue
        elif choice == '2':
            print("Returning to Faculty Landing Page...")
            faculty_landing()
            break
        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_login():
    while True:
        print("\nTA Login")

        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")

        print("\n1. Sign-In")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM User WHERE user_id=%s AND password=%s AND role=%s",
                    (user_id, password, 'ta'),
                )
                ta_user = cursor.fetchone()

                if ta_user:
                    print("Login successful. Redirecting to TA Landing Page...")
                    ta_id = ta_user[0]
                    ta_landing_page(ta_id)
                else:
                    print(
                        "Login Incorrect. Please check your credentials and try again."
                    )

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Going back to the Home page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_landing_page(ta_id):
    while True:
        print("\nTA Landing Page")
        print("1. Go to Active Course")
        print("2. View Courses")
        print("3. Change Password")
        print("4. Logout")

        choice = input("Enter choice (1-4): ")

        if choice == '1':
            ta_go_to_active_course(ta_id)
        elif choice == '2':
            ta_view_courses(ta_id)
        elif choice == '3':
            ta_change_password(ta_id)
        elif choice == '4':
            print("Logging out... Returning to the Home page.")
            return main_menu()
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


def ta_go_to_active_course(ta_id):
    while True:

        course_id = input("Enter the Active Course ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.textbook_id FROM Course c JOIN TeachingAssistant t ON t.course_id = c.course_id WHERE c.course_type = 'active' AND t.teaching_assistant_id = %s AND c.course_id = %s",
            (
                ta_id,
                course_id,
            ),
        )
        textbook_id = cursor.fetchone()[0]

        print("\nTA: Active Course Menu")
        print("1. View Students")
        print("2. Add New Chapter")
        print("3. Modify Chapters")
        print("4. Go Back")

        choice = input("Enter choice (1-4): ")

        if choice == '1':

            ta_view_students(ta_id)
        elif choice == '2':

            ta_add_new_chapter(ta_id, textbook_id)
        elif choice == '3':

            ta_modify_chapter(textbook_id, ta_id)
        elif choice == '4':

            print("Going back to the previous page...")
            return
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


def ta_view_courses(ta_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT t.course_id, c.title FROM TeachingAssistant t JOIN Course c ON c.course_id = t.course_id WHERE t.teaching_assistant_id = %s",
            (ta_id,),
        )
        courses = cursor.fetchall()

        if courses:
            print("\nAssigned Courses:")
            for course_id, course_title in courses:
                print(f"Course ID: {course_id}, Course Name: {course_title}")
        else:
            print("No courses assigned.")

        print("\n1. Go Back")
        choice = input("Choose an option: ")
        if choice == '1':
            print("Going back to TA landing page...")

            ta_landing_page(ta_id)
        else:
            print("Invalid option, please try again.")
            view_courses(ta_id)
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        cursor.close()
        conn.close()


def ta_change_password(ta_id):
    while True:
        print("\nChange Password")
        current_password = input("Enter current password: ")
        new_password = input("Enter new password: ")
        confirm_new_password = input("Confirm new password: ")

        print("\n1. Update")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            if new_password != confirm_new_password:
                print("New passwords do not match. Please try again.")
                continue

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT password FROM User WHERE user_id=%s AND role='ta'", (ta_id,)
                )
                actual_current_password = cursor.fetchone()[0]

                if actual_current_password == current_password:

                    cursor.execute(
                        "UPDATE User SET password=%s WHERE user_id=%s AND role='ta'",
                        (new_password, ta_id),
                    )
                    conn.commit()
                    print("Password updated successfully!")
                else:
                    print("Current password is incorrect. Please try again.")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

            break

        elif choice == '2':
            print("Cancelling and going back to the previous page...")
            break

        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_view_students(ta_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT course_id FROM TeachingAssistant WHERE teaching_assistant_id=%s",
            (ta_id,),
        )
        courses = cursor.fetchall()
        if not courses:
            print("You are not assigned to any courses.")
            return

        for course in courses:
            course_id = course[0]
            print(f"\nStudents in Course ID {course_id}:")
            cursor.execute(
                """
                SELECT DISTINCT e.student_id, CONCAT(u.first_name, " ", u.last_name) as name, e.status
                FROM Enrollment e
                JOIN User u ON u.user_id = e.student_id
                WHERE course_id=%s
            """,
                (course_id,),
            )
            students = cursor.fetchall()
            if students:
                for student_id, name, status in students:
                    print(f"Student ID: {student_id}, Name: {name}, Status: {status}")
            else:
                print(f"No students found in Course ID {course_id}.")

        print("\n1. Go Back")
        choice = input("Choose an option: ")
        if choice == '1':
            print("Going back to TA landing page...")

            ta_landing_page(ta_id)
        else:
            print("Invalid option, please try again.")
            ta_view_students(ta_id)
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        cursor.close()
        conn.close()


def ta_add_new_chapter(ta_id, textbook_id):
    print("\nAdd New Chapter")
    chapter_id = input("Enter Unique Chapter ID: ")
    chapter_title = input("Enter Chapter Title: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO Chapter(chapter_id, title, textbook_id) VALUES (%s, %s, %s)",
            (chapter_id, chapter_title, textbook_id),
        )
        conn.commit()
        print("Chapter added successfully.")

        while True:
            print("\n1. Add New Section")
            print("2. Go Back")
            choice = input("Choose an option (1-2): ")

            if choice == '1':
                ta_add_new_section(chapter_id, textbook_id, ta_id)

            elif choice == '2':
                print("Returning to the previous menu...")
                return ta_go_to_active_course(ta_id)
            else:
                print("Invalid choice. Please select either 1 or 2.")

    except mysql.connector.Error as err:
        if "chapter_id must be in the format" in str(err):
            print(f"Error: {err}")
            print("Please enter a valid chapter_id in the format 'chap[0-9][1-9]'.")
        else:
            print(f"An error occurred: {err}")
            conn.rollback()

    finally:
        cursor.close()
        conn.close()


def ta_add_new_section(chapter_id, textbook_id, ta_id):
    print("\nAdd New Section")
    section_number = input("Enter Section Number: ")
    section_title = input("Enter Section Title: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT * FROM Section WHERE section_number=%s AND chapter_id=%s AND textbook_id = %s",
            (section_number, chapter_id, textbook_id),
        )
        if cursor.fetchone():
            print(
                "Section already exists with this number. Please try another section number."
            )
            return ta_add_new_section(chapter_id, textbook_id, ta_id)
        else:

            print("\n1. Add New Content Block")
            print("2. Go Back")
            choice = input("Choose an option (1-2): ")

            if choice == '1':

                cursor.execute(
                    """
                    INSERT INTO Section (section_number, title, chapter_id,textbook_id)
                    VALUES (%s, %s, %s, %s)
                """,
                    (section_number, section_title, chapter_id, textbook_id),
                )
                conn.commit()
                print(
                    "Section created successfully! Redirecting to Add New Content Block..."
                )
                cursor.execute(
                    "SELECT section_id FROM Section WHERE chapter_id = %s AND textbook_id = %s AND section_number = %s",
                    (chapter_id, textbook_id, section_number),
                )
                section_id = cursor.fetchone()[0]
                return ta_add_new_content_block(
                    chapter_id, section_id, ta_id, textbook_id
                )
            elif choice == '2':
                print("Going back to the previous menu...")
                return ta_add_new_chapter(ta_id, textbook_id)
            else:
                print("Invalid choice. Please select either 1 or 2.")

    except mysql.connector.Error as err:
        if "section_number must be in the format" in str(err):
            print(f"Error: {err}")
            print("Please enter a valid section_number in the format 'sec[0-9][1-9]'.")
        else:
            print(f"An error occurred: {err}")
    finally:
        cursor.close()
        conn.close()


def ta_modify_chapter(textbook_id, ta_id):
    print("\nModify Chapter")
    chapter_id = input("Enter Unique Chapter ID: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s",
            (chapter_id, textbook_id),
        )
        chapter = cursor.fetchone()[0]
        if not chapter:
            print("The chapter ID does not exist. Please enter a valid Chapter ID.")
            return
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        return
    finally:
        cursor.close()
        conn.close()

    while True:
        print("\n1. Add New Section")
        print("2. Modify Section")
        print("3. Go Back")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            ta_add_new_section(chapter_id, textbook_id, ta_id)
        elif choice == '2':
            ta_modify_section(chapter_id, textbook_id, ta_id)
        elif choice == '3':
            print("Returning to the previous menu...")
            break
        else:
            print("Invalid choice. Please select either 1, 2, or 3.")


def ta_add_new_content_block(chapter_id, section_id, ta_id, textbook_id):
    while True:
        print("\nAdd New Content Block")
        content_block_id = input("Enter Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s",
                (content_block_id,),
            )
            (count,) = cursor.fetchone()
            if count > 0:
                print(
                    "A content block with this ID already exists. Please try a different ID."
                )
                continue
            else:
                cursor.execute(
                    "INSERT INTO ContentBlock (content_block_id, section_id) VALUES (%s, %s)",
                    (
                        content_block_id,
                        section_id,
                    ),
                )
                conn.commit()
        except mysql.connector.Error as err:
            if "content_block_id must be in the format" in str(err):
                print(f"Error: {err}")
                print(
                    "Please enter a valid Content Block ID the format 'sec[0-9][1-9]'."
                )
            else:
                print(f"An error occurred: {err}")
                continue
        finally:
            cursor.close()
            conn.close()

        print("1. Add Text")
        print("2. Add Picture")
        print("3. Add Activity")
        print("4. Hide Activity")
        print("5. Go Back")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            ta_add_text(content_block_id, section_id)
        elif choice == '2':
            ta_add_picture(content_block_id, section_id)
        elif choice == '3':
            ta_add_new_activity(content_block_id, section_id)
        elif choice == '4':
            ta_hide_activity(content_block_id, section_id)
        elif choice == '5':
            print("Going back to the previous menu...")
            return ta_add_new_section(chapter_id, textbook_id, ta_id)
        else:
            print("Invalid choice. Please select a number between 1 and 5.")


def ta_hide_activity(content_block_id, section_id):
    while True:
        print("\nHide Activity")

        activity_id = input("Enter the unique Activity ID: ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT * FROM Activity WHERE activity_id=%s AND section_id = %s AND content_block_id = %s",
                    (
                        activity_id,
                        section_id,
                        content_block_id,
                    ),
                )
                activity = cursor.fetchone()

                if activity:

                    cursor.execute(
                        """
                        UPDATE Activity
                        SET hidden = 'yes'
                        WHERE activity_id = %s AND section_id = %s AND content_block_id = %s
                    """,
                        (activity_id, section_id, content_block_id),
                    )
                    conn.commit()
                    print("Activity hidden successfully!")
                else:
                    print(f"No activity found with ID: {activity_id}")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_add_text(content_block_id, section_id):
    while True:
        print("\nAdd Text to Content Block")
        text_input = input("Enter the text to add: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:

                cursor.execute(
                    "UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s",
                    ('text', text_input, content_block_id, section_id),
                )
                conn.commit()
                print("Text has been added successfully to the content block.")
                return
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Going back to the previous page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_add_picture(content_block_id, section_id):
    while True:
        print("\nAdd Picture to Content Block")

        picture_path = input("Enter the file path or URL of the picture: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:

                cursor.execute(
                    "UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s",
                    ('picture', picture_path, content_block_id, section_id),
                )
                conn.commit()
                print("Picture has been added successfully to the content block.")
                return
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Going back to the previous page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_add_new_activity(content_block_id, section_id):
    while True:
        print("\nAdd Activity")

        activity_id = input("Enter the Unique Activity ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO Activity (activity_id, content_block_id, section_id)
                VALUES (%s, %s, %s)
            """,
                (
                    activity_id,
                    content_block_id,
                    section_id,
                ),
            )
            conn.commit()
            print(
                f"Activity with ID {activity_id} added successfully to Content Block {content_block_id}."
            )

        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add Question")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            print(f"Redirecting to Add Question page for Activity ID: {activity_id}...")
            ta_add_question(activity_id, content_block_id, section_id)
            return
        elif choice == '2':

            print("Going back to the previous page...")
            return
        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_add_question(activity_id, content_block_id, section_id):
    while True:
        print("\nAdd Question")

        question_id = input("Enter Question ID: ")
        question_text = input("Enter Question Text: ")

        option1_text = input("Enter Option 1 Text: ")
        option1_explanation = input("Enter Option 1 Explanation: ")

        option2_text = input("Enter Option 2 Text: ")
        option2_explanation = input("Enter Option 2 Explanation: ")

        option3_text = input("Enter Option 3 Text: ")
        option3_explanation = input("Enter Option 3 Explanation: ")

        option4_text = input("Enter Option 4 Text: ")
        option4_explanation = input("Enter Option 4 Explanation: ")

        correct_option = input("Enter Correct Option (1-4): ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    """
                    INSERT INTO Question (question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option, activity_id, section_id, content_block_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        question_id,
                        question_text,
                        option1_text,
                        option2_text,
                        option3_text,
                        option4_text,
                        option1_explanation,
                        option2_explanation,
                        option3_explanation,
                        option4_explanation,
                        correct_option,
                        activity_id,
                        section_id,
                        content_block_id,
                    ),
                )
                conn.commit()
                print("Question and options added successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return ta_add_new_activity(content_block_id, section_id)

        elif choice == '2':
            print("Discarding input. Returning to Add Activity page...")
            return ta_add_new_activity(content_block_id, section_id)
        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_modify_section(chapter_id, textbook_id, ta_id):
    while True:
        print("\nModify Section")

        section_number = input("Enter Section Number: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT section_id FROM Section
                WHERE section_number = %s AND chapter_id = %s AND textbook_id = %s
            """,
                (section_number, chapter_id, textbook_id),
            )
            section_id = cursor.fetchone()[0]

            if not section_id:
                print(f"Section {section_number} does not exist. Please try again.")
                return
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            return
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add New Content Block")
        print("2. Modify Content Block")
        print("3. Delete Content Block")
        print("4. Hide Content Block")
        print("5. Go Back")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            print("Adding new content block...")

            ta_add_new_content_block(chapter_id, section_id, ta_id, textbook_id)

        elif choice == '2':
            print("Modifying content block...")

            ta_modify_content_block(section_id, ta_id)

        elif choice == '3':
            print("Deleting content block...")

            ta_delete_content_block(section_id)

        elif choice == '4':
            print("Hiding content block...")

            ta_hide_content_block(section_id)

        elif choice == '5':
            print("Going back to the previous page...")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 5.")


def ta_modify_content_block(section_id, ta_id):
    while True:
        print("\nModify Content Block")

        content_block_id = input("Enter Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s AND section_id = %s",
                (
                    content_block_id,
                    section_id,
                ),
            )
            (count,) = cursor.fetchone()
            if count == 0:
                print(
                    "This content block does not exist. Please check the details or create a new content block."
                )
                continue
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add Text")
        print("2. Add Picture")
        print("3. Add Activity")
        print("4. Go Back")
        print("5. Landing Page")

        choice = input("Enter choice (1-5): ")

        if choice == '1':
            print("Adding Text...")

            ta_add_text(content_block_id, section_id)

        elif choice == '2':
            print("Adding Picture...")

            ta_add_picture(content_block_id, section_id)

        elif choice == '3':
            print("Adding Activity...")

            ta_add_new_activity(content_block_id, section_id)

        elif choice == '4':
            print("Going back to the previous page...")
            break

        elif choice == '5':
            print("Redirecting to User Landing Page...")

            ta_landing_page()
            break

        else:
            print("Invalid choice. Please select a number between 1 and 5.")


def ta_delete_content_block(section_id):
    while True:
        print("\nDelete Content Block")

        content_block_id = input("Enter Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s AND section_id = %s",
                (
                    content_block_id,
                    section_id,
                ),
            )
            (count,) = cursor.fetchone()
            if count == 0:
                print(
                    "This content block does not exist. Please check the ID or go back."
                )
                continue
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        print("\n1. Delete")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "DELETE FROM ContentBlock WHERE content_block_id = %s AND section_id = %s",
                    (
                        content_block_id,
                        section_id,
                    ),
                )
                conn.commit()
                print(
                    f"Content Block with ID {content_block_id} has been deleted successfully."
                )
            except mysql.connector.Error as err:
                print(f"An error occurred while deleting: {err}")
            finally:
                cursor.close()
                conn.close()
            print("Returning to the previous page...")

        elif choice == '2':
            print("Going back to the previous page...")
            break

        else:
            print("Invalid choice. Please select either 1 or 2.")


def ta_hide_content_block(section_id):
    while True:
        print("\nHide Content Block")

        content_block_id = input("Enter Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s AND section_id = %s",
                (
                    content_block_id,
                    section_id,
                ),
            )
            (count,) = cursor.fetchone()
            if count == 0:
                print(
                    "This content block does not exist. Please check the ID or go back."
                )
                continue
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        print("\n1. Hide")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE ContentBlock SET hidden = 'yes' WHERE content_block_id = %s and section_id = %s",
                    (content_block_id, section_id),
                )
                conn.commit()
                print(
                    f"Content Block with ID {content_block_id} has been hidden successfully."
                )
            except mysql.connector.Error as err:
                print(f"An error occurred while hiding: {err}")
            finally:
                cursor.close()
                conn.close()
            print("Returning to the previous page...")

        elif choice == '2':
            print("Going back to the previous page...")
            break

        else:
            print("Invalid choice. Please select either 1 or 2.")


def student_login():
    while True:
        print("\nStudent Login Menu")
        print("1. Enroll in a Course")
        print("2. Sign-In")
        print("3. Go Back")

        choice = input("Choose an option (1-3): ")

        if choice == '1':

            enroll_in_course()
        elif choice == '2':

            student_sign_in()
        elif choice == '3':

            print("Going back to the Home page...")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")


def enroll_in_course():
    while True:
        print("\nStudent Enrollment")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        course_token = input("Enter Course Token: ")

        print("\n1. Enroll")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:

                cursor.execute(
                    "SELECT user_id FROM User WHERE email=%s AND role = 'student'",
                    (email,),
                )
                student_id = cursor.fetchone()

                cursor.execute(
                    "SELECT course_id FROM Course WHERE course_token=%s AND course_type = 'active'",
                    (course_token,),
                )
                course_id = cursor.fetchone()

                if not course_id:
                    print(f"Invalid course token.")
                    continue

                course_id = course_id[0]

                if student_id:

                    student_id = student_id[0]
                    print(
                        f"Student already exists. Adding to course with token {course_token}."
                    )
                    cursor.execute(
                        "INSERT INTO Enrollment (student_id, course_id, status) VALUES (%s, %s, %s)",
                        (student_id, course_id, 'pending'),
                    )
                else:

                    print(
                        f"Creating a new student and adding to course with token {course_token}."
                    )
                    user_id_prefix = first_name[:2] + last_name[:2]
                    current_date = datetime.now()
                    user_id_date = current_date.strftime("%y%m")
                    student_id = user_id_prefix + user_id_date
                    print(f"Generated User ID: {student_id}")
                    cursor.execute(
                        "INSERT INTO User (user_id, first_name, last_name, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            student_id,
                            first_name,
                            last_name,
                            email,
                            'defaultpassword',
                            'student',
                        ),
                    )
                    cursor.execute(
                        "INSERT INTO Student (student_id) VALUES (%s)", (student_id,)
                    )
                    cursor.execute(
                        "INSERT INTO Enrollment (student_id, course_id, status) VALUES (%s, %s, %s)",
                        (student_id, course_id, 'pending'),
                    )

                conn.commit()
                print(
                    f"Enrollment request submitted. You have been added to the waiting list for course {course_token}."
                )

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Going back to the Login page...")
            break

        else:
            print("Invalid choice. Please select 1 or 2.")


def student_sign_in():
    while True:
        print("\nStudent Sign-In")

        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")

        print("\n1. Sign-In")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "SELECT * FROM User WHERE user_id=%s AND password=%s AND role='student'",
                    (user_id, password),
                )
                student = cursor.fetchone()

                if student:
                    print("Login successful. Redirecting to Student Landing Page...")

                    student_landing_page(student[0])
                else:
                    print(
                        "Login Incorrect. Please check your credentials and try again."
                    )

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':

            print("Going back to the Home page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def student_landing_page(student_id):
    while True:
        print("\nStudent Landing Page")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT c.textbook_id from course c WHERE c.course_id IN (SELECT DISTINCT e.course_id FROM enrollment e WHERE e.student_id = %s AND e.status='approved')",
            (student_id,),
        )
        textbook_ids = cursor.fetchall()
        for textbook_id in textbook_ids:
            print(f"E-book {textbook_id[0]}")
            cursor.execute(
                "SELECT chapter_id FROM Chapter WHERE textbook_id=%s", (textbook_id[0],)
            )
            chapter_ids = cursor.fetchall()
            for chapter_id in chapter_ids:
                print(f"Chapter {chapter_id[0]}")
                cursor.execute(
                    "SELECT section_id, section_number FROM Section WHERE textbook_id=%s AND chapter_id=%s",
                    (textbook_id[0], chapter_id[0]),
                )
                sections = cursor.fetchall()
                for section in sections:
                    print(f"\tSection {section[1]}")
                    cursor.execute(
                        "SELECT content_block_id FROM ContentBlock WHERE section_id=%s",
                        (section[0],),
                    )
                    block_ids = cursor.fetchall()
                    for block_id in block_ids:
                        print(f"\t\tBlock {block_id[0]}")

        print("\nMenu:")
        print("1. View a section")
        print("2. View participation activity point")
        print("3. Logout")

        choice = input("Choose an option (1-3): ")

        if choice == '1':

            view_section(student_id)
        elif choice == '2':

            view_participation_activity_point(student_id)
        elif choice == '3':

            print("Logging out... Returning to the home page.")
            return main_menu()
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def view_section(student_id):
    while True:
        print("\nView Section")
        textbook_id = input("Enter Textbook ID: ")
        chapter_id = input("Enter Chapter ID: ")
        section_num = input("Enter Section Number: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT section_id FROM Section WHERE textbook_id = %s AND chapter_id = %s AND section_number = %s",
                (textbook_id, chapter_id, section_num),
            )
            (section_id,) = cursor.fetchone()

            if not section_id:
                print("Invalid Chapter ID or Section ID. Please enter valid details.")
                continue

        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

        print("\nMenu:")
        print("1. View Block")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':

            view_block(textbook_id, chapter_id, section_id, student_id)
        elif choice == '2':
            print("Going back to the previous page...")
            return
        else:
            print("Invalid choice. Please select 1 or 2.")


def view_block(textbook_id, chapter_id, section_id, student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT content_block_id, block_type, content FROM ContentBlock WHERE section_id = %s",
            (section_id,),
        )
        blocks = cursor.fetchall()

        if not blocks:
            print(f"No blocks found for Section {section_id}")
            return

        for block_id, block_type, content in blocks:
            print(f"\nViewing Block {block_id}")
            if block_type == 'text' or block_type == 'picture':

                print(f"Content: {content}")
                print("1. Next")
                print("2. Go Back")
                choice = input("Choose an option (1-2): ")

                if choice == '1':
                    continue
                elif choice == '2':
                    print("Going back to the previous page...")
                    return
                else:
                    print("Invalid option. Please try again.")
                    return
            elif block_type == 'activity':
                print("Activity")
                activity_id = content
                cursor.execute(
                    "SELECT question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option FROM Question WHERE section_id = %s AND content_block_id = %s AND activity_id = %s",
                    (section_id, block_id, activity_id),
                )

                question = cursor.fetchone()

                question_id, question_text = question[0], question[1]
                options = [question[2], question[3], question[4], question[5]]
                explanations = [question[6], question[7], question[8], question[9]]
                correct_answer = question[10]

                tmp = cursor.fetchall()

                print(f"Question: {question_text}")

                print("Options:")
                for idx, option in enumerate(options):
                    print(f"{idx + 1}. {option}")

                user_answer = int(input("Enter the correct answer (1-4): "))

                print("1. Submit")
                print("2. Go Back")
                choice = input("Choose an option (1-2): ")

                cursor.execute(
                    "SELECT score_id FROM Score WHERE textbook_id=%s AND chapter_id=%s AND section_id=%s AND content_block_id=%s AND activity_id=%s AND question_id=%s AND student_id=%s",
                    (
                        textbook_id,
                        chapter_id,
                        section_id,
                        block_id,
                        activity_id,
                        question_id,
                        student_id,
                    ),
                )
                score = cursor.fetchone()

                if choice == '1':
                    current_timestamp = datetime.now()
                    current_timestamp = current_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    if user_answer < 1 and user_answer > 4:
                        print("Invalid choice.")
                        continue
                    elif int(user_answer) == int(correct_answer):
                        print("Correct! You score increased by 3.")
                        if score:

                            cursor.execute(
                                f"UPDATE Score SET score = 3, timestamp = '{current_timestamp}' WHERE textbook_id={textbook_id} AND chapter_id='{chapter_id}' AND section_id={section_id} AND content_block_id='{block_id}' AND activity_id='{activity_id}' AND question_id='{question_id}'"
                            )
                        else:
                            course_id = input("Enter Course ID: ")
                            cursor.execute(
                                f"INSERT INTO Score(student_id, course_id, textbook_id, section_id, chapter_id, content_block_id, activity_id, question_id, score, feedback, timestamp) VALUES('{student_id}', '{course_id}', '{textbook_id}', '{section_id}', '{chapter_id}', '{block_id}', '{activity_id}', '{question_id}', 3, '', '{current_timestamp}')"
                            )
                        conn.commit()
                    else:
                        print(
                            "Incorrect answer. You lost 1 point. Here's the explanation..."
                        )
                        explanation = explanations[int(correct_answer) - 1]
                        print(explanation)
                        if score:

                            cursor.execute(
                                f"UPDATE Score SET score = -1, timestamp = '{current_timestamp}' WHERE textbook_id={textbook_id} AND chapter_id='{chapter_id}' AND section_id={section_id} AND content_block_id='{block_id}' AND activity_id='{activity_id}' AND question_id='{question_id}'"
                            )
                        else:
                            course_id = input("Enter Course ID: ")
                            cursor.execute(
                                f"INSERT INTO Score(student_id, course_id, textbook_id, section_id, chapter_id, content_block_id, activity_id, question_id, score, feedback, timestamp) VALUES('{student_id}', '{course_id}', '{textbook_id}', '{section_id}', '{chapter_id}', '{block_id}', '{activity_id}', '{question_id}', -1, '', '{current_timestamp}')"
                            )
                        conn.commit()
                    continue
                elif choice == '2':
                    print("Going back to the previous page...")
                    return
                else:
                    print("Invalid option. Please try again.")
                    return
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        cursor.close()
        conn.close()
        return student_landing_page(student_id)


def view_participation_activity_point(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "SELECT SUM(score) FROM Score WHERE student_id = %s", (student_id,)
        )
        result = cursor.fetchone()

        if result:
            participation_points = result[0]
            print(f"\nCurrent Participation Points")
            print(
                f"Your current total participation activity points: {participation_points}"
            )
        else:
            print("No participation points found for this student.")

        print("\n1. Go back")
        choice = input("Choose an option (1): ")

        if choice == '1':
            print("Going back to the landing page...")
            return
        else:
            print("Invalid option. Returning to the landing page...")
            return

    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        cursor.close()
        conn.close()


def student_home():
    print("Student Home")


if __name__ == '__main__':
    main_menu()
