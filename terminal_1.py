import mysql.connector
from datetime import datetime

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="springstudent",  # Replace with your username
        password="springstudent",  # Replace with your password
        database="proj1"  # Replace with your database name
    )

def start_menu():
    while True:
        print("\n===== Main Menu =====")
        print("1. Admin Login")
        print("2. Faculty Login")
        print("3. TA Login")
        print("4. Student Login")
        print("5. Exit")

        choice = input("Enter Choice (1-5): ")

        if choice == '1':
            login('admin')
        elif choice == '2':
            login('faculty')
        elif choice == '3':
            login('ta')
        elif choice == '4':
            student_login()
        elif choice == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


def login(user_type):
    while True:
        print(f"\n===== {user_type.capitalize()} Login =====")
        print("1. Sign-In")
        print("2. Go Back")

        # Take the user's choice
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Proceed with the Sign-In process
            user_id = input("Enter User ID: ")
            password = input("Enter Password: ")

            # Connect to the database and validate the credentials
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE user_id=%s AND password=%s AND role=%s", (user_id, password, user_type))
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
                break  # Exit the loop after successful login
            else:
                print("Login failed. Incorrect credentials.")

            cursor.close()
            conn.close()

        elif choice == '2':
            # Discard input and go back to the home page
            print("Going back to the Main Menu...")
            return start_menu()  # Redirects back to the start menu

        else:
            print("Invalid choice. Please enter 1 or 2.")

def admin_home():
    while True:
        print("\n===== Admin Landing Menu =====")
        print("1. Create a Faculty Account")
        print("2. Create E-textbook")
        print("3. Modify E-textbooks")
        print("4. Create New Active Course")
        print("5. Create New Evaluation Course")
        print("6. Logout")

        # Take input from the admin
        choice = input("Enter choice (1-6): ")

        if choice == '1':
            create_faculty_account()
        elif choice == '2':
            create_e_textbook()
        elif choice == '3':
            modify_etextbook()
        elif choice == '4':
            create_new_active_course()
        elif choice == '5':
            create_new_eval_course()
        elif choice == '6':
            print("Logging out... Returning to the Home page.")
            start_menu()  # Redirect to start menu or exit the loop
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def create_faculty_account():
    while True:
        print("\n===== Create a Faculty Account =====")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        password = input("Enter Password: ")

        # Generate user_id based on the provided logic
        user_id_prefix = first_name[:2] + last_name[:2]
        current_date = datetime.now()
        user_id_date = current_date.strftime("%y%m")
        user_id = user_id_prefix + user_id_date
        print(f"Generated User ID: {user_id}")
        
        print("\n1. Add User")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Attempt to add user to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if email already exists
                cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    print("A user with this email already exists. Please try again with a different email.")
                else:
                    # Insert new faculty into User table
                    cursor.execute("""
                        INSERT INTO User (user_id, first_name, last_name, email, password, role)
                        VALUES (%s, %s, %s, %s, %s, 'faculty')
                    """, (user_id, first_name, last_name, email, password))
                    
                    # Insert into Faculty table using the same user_id as faculty_id
                    cursor.execute("""
                        INSERT INTO Faculty (faculty_id)
                        VALUES (%s)
                    """, (user_id,))
                    
                    # Commit the transaction
                    conn.commit()
                    print("Faculty account created successfully in both User and Faculty tables!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return  # Go back to the admin landing page after adding user

        elif choice == '2':
            # Go back to the admin landing page without saving
            print("Discarding input. Returning to Admin Landing Page...")
            return  # Return to the Admin Landing Page
        else:
            print("Invalid choice. Please select 1 or 2.")

# def create_faculty_account():
#     while True:
#         print("\n===== Create a Faculty Account =====")
#         first_name = input("Enter First Name: ")
#         last_name = input("Enter Last Name: ")
#         email = input("Enter Email: ")
#         password = input("Enter Password: ")
#         user_id_prefix = first_name[:2] + last_name[:2]
#         current_date = datetime.now()
#         user_id_date = current_date.strftime("%y%m")
#         user_id = user_id_prefix + user_id_date
#         print(user_id)
        
# ## Add-1 Create a trigger for this user creation

#         print("\n1. Add User")
#         print("2. Go Back")
#         choice = input("Enter choice (1-2): ")

#         if choice == '1':
#             # Attempt to add user to the database
            
#             conn = get_db_connection()
#             cursor = conn.cursor()

#             try:
#                 # Check if email already exists
#                 cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
#                 existing_user = cursor.fetchone()

#                 if existing_user:
#                     print("A user with this email already exists. Please try again with a different email.")
#                 else:
#                     # Insert new faculty into the database
#                     cursor.execute("""
#                         INSERT INTO User (user_id, first_name, last_name, email, password, role)
#                         VALUES (%s, %s, %s, %s, %s, 'faculty')
#                     """, (user_id, first_name, last_name, email, password))
#                     conn.commit()
#                     print("Faculty account created successfully!")
#             except mysql.connector.Error as err:
#                 print(f"An error occurred: {err}")
#             finally:
#                 cursor.close()
#                 conn.close()
#             return  # Go back to the admin landing page after adding user

#         elif choice == '2':
#             # Go back to the admin landing page without saving
#             print("Discarding input. Returning to Admin Landing Page...")
#             return  # Return to the Admin Landing Page
#         else:
#             print("Invalid choice. Please select 1 or 2.")


def create_e_textbook():
    while True:
        print("\n===== Create E-textbook =====")
        title = input("Enter the title of the new E-textbook: ")
        textbook_id = input("Enter the unique E-textbook ID: ")

        print("\n1. Add New Chapter")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to add a new chapter for the created E-textbook
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the E-textbook ID already exists
                cursor.execute("SELECT * FROM ETextbook WHERE textbook_id=%s", (textbook_id,))
                existing_textbook = cursor.fetchone()

                if existing_textbook:
                    print("A textbook with this ID already exists. Please try again with a different ID.")
                else:
                    # Insert the new textbook into the database
                    cursor.execute("""
                        INSERT INTO ETextbook (textbook_id, title)
                        VALUES (%s, %s)
                    """, (textbook_id, title))
                    conn.commit()
                    print("E-textbook created successfully!")
                    add_new_chapter(textbook_id)  # Redirect to add new chapter function
                    return # Go back to the admin landing page after chapter addition
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Go back to the admin landing page without saving
            print("Discarding input. Returning to Admin Landing Page...")
            return  # Return to the Admin Landing Page
        else:
            print("Invalid choice. Please select 1 or 2.")

def add_new_chapter(textbook_id):
    while True:
        print(f"\n===== Add New Chapter to E-textbook (ID: {textbook_id}) =====")
        chapter_id = input("Enter Unique Chapter ID: ")
        chapter_title = input("Enter Chapter Title: ")
        # chapter_number = input("Enter Chapter Number: ")
        print("\n1. Add New Section")
        print("2. Go Back")
        print("3. Landing Page")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            # Proceed to add a new section for the chapter
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Insert the new chapter into the database
                cursor.execute("""
                    INSERT INTO Chapter (chapter_id, title, textbook_id)
                    VALUES (%s, %s, %s)
                """, (chapter_id, chapter_title, textbook_id))
                conn.commit()
                print("Chapter added successfully!")
                return add_new_section(chapter_id, textbook_id)
                # if role ==  'admin':
                #     return add_new_section(chapter_id, textbook_id) # Redirect to add new section function
                # elif role == 'faculty':
                #     return add_new_section(chapter_id, textbook_id, 'faculty')
                # elif role == 'ta':
                #     return add_new_section(chapter_id, textbook_id, 'ta')
            except mysql.connector.Error as err:
                if "chapter_id must be in the format" in str(err):
                    print(f"Error: {err}")
                    print("Please enter a valid chapter_id in the format 'chap[0-9][1-9]'.")
                else:
                    print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Go back to the previous page without saving
            print("Discarding input. Returning to the previous page...")
            # if role ==  'admin':
            return create_e_textbook()  # Return to the previous page
            # elif role == 'faculty':
                # faculty_landing()

        elif choice == '3':
            # Go back to the Admin Landing Page without saving
            print("Discarding input. Returning to the Admin Landing Page...")
            return admin_home() # Return to the Admin Landing Page

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def add_new_section(chapter_id,textbook_id):
    while True:
        print(f"\n===== Add New Section to Chapter (ID: {chapter_id}) =====")

        # Check if the chapter ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to check if the chapter exists
        cursor.execute("SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s", (chapter_id, textbook_id))
        chapter = cursor.fetchone()

        if not chapter:
            print(f"Chapter with ID {chapter_id} does not exist. Please enter a valid Chapter ID.")
            cursor.close()
            conn.close()
            break  # Return to the previous menu
        else:
            print(f"Chapter with ID {chapter_id} found.")
            cursor.close()
            conn.close()

        # section_id = input("Enter Unique Section ID: ")
        section_number = input("Enter Section Number: ")
        section_title = input("Enter Section Title: ")

        print("\n1. Add New Content Block")
        print("2. Go Back")
        print("3. Landing Page")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            # Redirect to add a new content block
            # Proceed to add a new section for the chapter
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                # Insert the new section into the database with textbook_id
                cursor.execute("""
                    INSERT INTO Section (title, chapter_id, section_number, textbook_id)
                    VALUES (%s, %s, %s, %s)
                """, (section_title, chapter_id, section_number, textbook_id))
                conn.commit()

                cursor.execute("SELECT section_id FROM Section WHERE chapter_id = %s AND textbook_id = %s AND section_number = %s", (chapter_id, textbook_id, section_number))
                section_id = cursor.fetchone()[0]

                print("Section added successfully!")
                
                # Redirect to add a new content block after adding the section
                # return add_new_content_block(section_id)
                # if role ==  'admin':
                return add_new_content_block(section_id) # Redirect to add new section function
            except mysql.connector.Error as err:
                if "section_number must be in the format" in str(err):
                    print(f"Error: {err}")
                    print("Please enter a valid section_number in the format 'sec[0-9][1-9]'.")
                else:
                    print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Go back to the previous page without saving
            print("Returning to the previous page...")
            return add_new_chapter(textbook_id)

        elif choice == '3':
            # Go back to the landing page without saving
            print("Returning to the Admin Landing Page...")
            return admin_home()

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

# def add_new_section(chapter_id):
#     while True:
#         print(f"\n===== Add New Section to Chapter (ID: {chapter_id}) =====")

#         # Check if the chapter ID exists in the database
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Query to check if the chapter exists
#         cursor.execute("SELECT * FROM Chapter WHERE chapter_id = %s", (chapter_id,))
#         chapter = cursor.fetchone()

#         if not chapter:
#             print(f"Chapter with ID {chapter_id} does not exist. Please enter a valid Chapter ID.")
#             cursor.close()
#             conn.close()
#             break  # Return to the previous menu
#         else:
#             print(f"Chapter with ID {chapter_id} found.")
#             cursor.close()
#             conn.close()

#         section_id = input("Enter Unique Section ID:")
#         section_number = input("Enter Section Number: ")
#         section_title = input("Enter Section Title: ")
        

#         print("\n1. Add New Content Block")
#         print("2. Go Back")
#         print("3. Landing Page")
#         choice = input("Enter choice (1-3): ")

#         if choice == '1':
#             # Redirect to add a new content block
#             # Proceed to add a new section for the chapter
#             conn = get_db_connection()
#             cursor = conn.cursor()
            
#             try:
#                 # Insert the new chapter into the database
#                 cursor.execute("""
#                     INSERT INTO Section (section_id, title, chapter_id, section_number)
#                     VALUES (%s, %s, %s, %s)
#                 """, (section_id, section_title, chapter_id, section_number))
#                 conn.commit()
#                 print("Chapter added successfully!")
#                 add_new_content_block(section_id)
#                 return  # Return to previous menu after adding content block
#             except mysql.connector.Error as err:
#                 print(f"An error occurred: {err}")
#             finally:
#                 cursor.close()
#                 conn.close()

#         elif choice == '2':
#             # Go back to the previous page without saving
#             print("Returning to the previous page...")
#             return

#         elif choice == '3':
#             # Go back to the landing page without saving
#             print("Returning to the Admin Landing Page...")
#             return

#         else:
#             print("Invalid choice. Please select 1, 2, or 3.")


def add_new_content_block(section_id):
    while True:
        print(f"\n===== Add New Content Block for Section (ID: {section_id}) =====")

        content_block_id =  input("Enter Unique Content Block ID:")

        # Automatically create a new content block
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO ContentBlock (content_block_id, section_id) VALUES (%s, %s)", (content_block_id, section_id,))
            conn.commit()
            print(f"New Content Block created with ID {content_block_id}.")
            # Menu for content block actions
            print("\n1. Add Text")
            print("2. Add Picture")
            print("3. Add Activity")
            print("4. Go Back")
            print("5. Landing Page")
            
            choice = input("Enter choice (1-5): ")
            if choice == '1':
                return add_text(content_block_id, section_id)  # Pass section_id to add_text
            elif choice == '2':
                return add_picture(content_block_id,section_id)
            elif choice == '3':
                return add_activity(content_block_id, section_id)
            elif choice == '4':
                cursor.execute("SELECT chapter_id, textbook_id FROM Section WHERE section_id = %s", (section_id,))
                result = cursor.fetchone()
                chapter_id, textbook_id = result
                print("Discarding input. Returning to the previous page...")
                return add_new_section(chapter_id, textbook_id) # Go back to the previous page
            elif choice == '5':
                print("Discarding input. Returning to the User Landing Page...")
                return admin_home() # Go back to the User Landing Page
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except mysql.connector.Error as err:
            if "content_block_id must be in the format" in str(err):
                print(f"Error: {err}")
                print("Please enter a valid Content Block ID the format 'sec[0-9][1-9]'.")
            else:
                print(f"An error occurred: {err}")
                cursor.close()
                conn.close()
                return   
        
        cursor.close()
        conn.close()


def add_text(content_block_id, section_id):
    while True:
        print(f"\n===== Add Text to Content Block (ID: {content_block_id}) =====")
        text_content = input("Enter text content: ")

        print("\n1. Add")
        print("2. Go Back")
        print("3. Landing Page")

        choice = input("Enter choice (1-3): ")

        if choice == '1':
            # Proceed to save text content to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s", ('text', text_content, content_block_id, section_id))
                conn.commit()
                print(f"Text content added to Content Block {content_block_id} successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

            return add_new_content_block(section_id) # Go back to the previous page after adding the text

        elif choice == '2':
            print("Discarding input. Returning to the previous page...")
            return add_new_content_block(section_id)

        elif choice == '3':
            print("Discarding input. Returning to the User Landing Page...")
            return admin_home()

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def add_picture(content_block_id,section_id):
    while True:
        print(f"\n===== Add Picture to Content Block (ID: {content_block_id}) =====")
        picture_url = input("Enter picture URL: ")

        print("\n1. Add")
        print("2. Go Back")
        print("3. Landing Page")

        choice = input("Enter choice (1-3): ")

        if choice == '1':
            # Proceed to save the picture URL to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Save picture URL as a content block in the database
                cursor.execute("UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s", ('picture', picture_url, content_block_id, section_id))
                conn.commit()
                print(f"Picture URL added to Content Block {content_block_id} successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

            return add_new_content_block(section_id) # Go back to the previous page after adding the picture

        elif choice == '2':
            # Discard input and go back to the previous page
            print("Discarding input. Returning to the previous page...")
            return add_new_content_block(section_id) # Return to the previous page

        elif choice == '3':
            # Discard input and return to the user landing page
            print("Discarding input. Returning to the User Landing Page...")
            return admin_home() # Return to the User Landing Page

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def add_activity(content_block_id, section_id):
    while True:
        print(f"\n===== Add Activity to Content Block (ID: {content_block_id}) =====")
        activity_id = input("Enter Unique Activity ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Activity (activity_id, content_block_id, section_id)
                VALUES (%s, %s, %s)
            """, (activity_id, content_block_id, section_id,))
            conn.commit()
            print(f"Activity with ID {activity_id} added successfully to Content Block {content_block_id}.")
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add Question")
        print("2. Go Back")
        print("3. Landing Page")

        choice = input("Enter choice (1-3): ")

        if choice == '1':
            add_question(activity_id, content_block_id, section_id)  # Add questions to this activity
            return  # Return to previous page after adding the question

        elif choice == '2':
            print("Discarding input. Returning to the previous page...")
            return add_new_content_block(section_id) # Return to the previous page

        elif choice == '3':
            print("Discarding input. Returning to the User Landing Page...")
            return admin_home() # Return to the User Landing Page

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def add_question(activity_id, content_block_id, section_id):
    while True:
        print("\n===== Add Question =====")

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
        print("3. Landing Page")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            # Insert the question into the Activity table
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO Question (question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option, activity_id, section_id, content_block_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (question_id, question_text, option1_text, option2_text, option3_text, option4_text, option1_explanation, option2_explanation, option3_explanation, option4_explanation, correct_option, activity_id, section_id, content_block_id))
                conn.commit()
                print("Question and options added successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return add_activity(content_block_id, section_id) # Go back to the previous menu after saving

        elif choice == '2':
            print("Discarding input. Returning to Add Activity page...")
            return add_activity(content_block_id, section_id) # Return to Add Activity page

        elif choice == '3':
            print("Discarding input. Returning to Admin Landing Page...")
            return  # Return to Admin Landing Page

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def add_question_faculty(activity_id, content_block_id, section_id, faculty_id):
    while True:
        print("\n===== Add Question =====")

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
            # Insert the question into the Activity table
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO Question (question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option, activity_id, section_id, content_block_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (question_id, question_text, option1_text, option2_text, option3_text, option4_text, option1_explanation, option2_explanation, option3_explanation, option4_explanation, correct_option, activity_id, section_id, content_block_id))
                conn.commit()
                print("Question and options added successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return add_activity_faculty(content_block_id, section_id, faculty_id) # Go back to the previous menu after saving

        elif choice == '2':
            print("Discarding input. Returning to Add Activity page...")
            return add_activity_faculty(content_block_id, section_id, faculty_id) # Return to Add Activity page
        else:
            print("Invalid choice. Please select 1 or 2.")




def modify_etextbook():
    while True:
        print("\n===== Modify E-textbook =====")
        textbook_id = input("Enter Unique E-textbook ID: ")

        # Check if the textbook ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to check if the textbook exists
        cursor.execute("SELECT * FROM ETextbook WHERE textbook_id = %s", (textbook_id,))
        textbook = cursor.fetchone()

        if not textbook:
            print(f"Textbook with ID {textbook_id} does not exist. Please enter a valid ID.")
            cursor.close()
            conn.close()
            continue  # Prompt the user to re-enter a valid textbook ID
        else:
            print(f"Textbook with ID {textbook_id} found.")
            cursor.close()
            conn.close()

        print("\n1. Add New Chapter")
        print("2. Modify Chapter")
        print("3. Go Back")
        print("4. Landing Page")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            # Redirect to add a new chapter
            add_new_chapter(textbook_id)
            return modify_etextbook() # Return to previous menu after adding the chapter

        elif choice == '2':
            # Redirect to modify an existing chapter
            modify_chapter(textbook_id)
            return modify_etextbook() # Return to previous menu after modifying the chapter

        elif choice == '3':
            # Go back to the previous page without saving
            print("Returning to the previous page...")
            return

        elif choice == '4':
            # Go back to the landing page without saving
            print("Returning to the Admin Landing Page...")
            return

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

def modify_chapter(textbook_id):
    while True:
        print(f"\n===== Modify Chapter for Textbook (ID: {textbook_id}) =====")
        chapter_id = input("Enter Unique Chapter ID: ")

        # Check if the chapter ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to check if the chapter exists
        cursor.execute("SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s", (chapter_id, textbook_id))
        chapter = cursor.fetchone()

        if not chapter:
            print(f"Chapter with ID {chapter_id} does not exist for Textbook ID {textbook_id}. Please enter a valid Chapter ID.")
            cursor.close()
            conn.close()
            break  # Return to the previous menu
        else:
            print(f"Chapter with ID {chapter_id} found.")
            cursor.close()
            conn.close()

        print("\n1. Add New Section")
        print("2. Modify Section")
        print("3. Go Back")
        print("4. Landing Page")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            # Redirect to add new section
            add_new_section(chapter_id,textbook_id)
            return modify_chapter(textbook_id) # Return after handling section addition

        elif choice == '2':
            # Redirect to modify an existing section
            modify_section(chapter_id,textbook_id)
            return modify_chapter(textbook_id)  # Return after handling section modification

        elif choice == '3':
            # Go back to the previous page
            print("Returning to the previous page...")
            return

        elif choice == '4':
            # Go back to the Admin Landing Page
            print("Returning to the Admin Landing Page...")
            return

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


def modify_section(chapter_id,textbook_id):
    while True:
        print("\n===== Modify Section =====")

        section_num = input("Enter Section Number: ")

        # Validate the E-textbook ID, Chapter ID, and Section Number
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the E-textbook, chapter, and section exist in the database
            cursor.execute("""
                SELECT section_id FROM Section
                WHERE section_number = %s AND chapter_id = %s AND textbook_id = %s
            """, (section_num, chapter_id, textbook_id))

            section_id = cursor.fetchone()[0]

            if not section_id:
                print("Section not found for the given E-textbook ID, Chapter ID, and Section number. Please try again.")
                continue
            else:
                print("Section found successfully!")

                # Display menu options for modifying the section
                print("\n1. Add New Content Block")
                print("2. Modify Content Block")
                print("3. Go Back")
                print("4. Landing Page")

                choice = input("Enter choice (1-4): ")

                if choice == '1':
                    add_new_content_block(section_id)
                    return modify_section(chapter_id, textbook_id) # Go back after adding the content block

                elif choice == '2':
                    modify_content_block(section_id)
                    return modify_section(chapter_id, textbook_id) # Go back after modifying the content block

                elif choice == '3':
                    print("Returning to the previous page...")
                    return  # Return to the previous page

                elif choice == '4':
                    print("Returning to the Admin Landing Page...")
                    return  # Return to the Admin Landing Page

                else:
                    print("Invalid choice. Please select a number between 1 and 4.")
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

def modify_content_block(section_id):
    while True:
        print("\n===== Modify Content Block =====")
        content_block_id = input("Enter Content Block ID: ")

        # Validate the Content Block ID
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the Content Block exists in the database
            cursor.execute("SELECT * FROM ContentBlock WHERE content_block_id = %s", (content_block_id,))
            content_block = cursor.fetchone()

            if not content_block:
                print("Content Block not found for the given ID. Please try again.")
            else:
                print("Content Block found successfully!")

                # Display menu options for modifying the content block
                print("\n1. Add Text")
                print("2. Add Picture")
                print("3. Add New Activity")
                print("4. Go Back")
                print("5. Landing Page")

                choice = input("Enter choice (1-5): ")

                if choice == '1':
                    add_text(content_block_id,section_id)
                    return modify_content_block(section_id) # Return after adding text

                elif choice == '2':
                    add_picture(content_block_id,section_id)
                    return modify_content_block(section_id) # Return after adding a picture

                elif choice == '3':
                    add_activity(content_block_id)
                    return modify_content_block(section_id) # Return after adding an activity

                elif choice == '4':
                    print("Returning to the previous page...")
                    return  # Return to the previous page

                elif choice == '5':
                    print("Returning to the Admin Landing Page...")
                    return  # Return to the Admin Landing Page

                else:
                    print("Invalid choice. Please select a number between 1 and 5.")
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()


def create_new_active_course():
    while True:
        print("\n===== Create New Active Course =====")
        course_id = input("Enter Unique Course ID: ")
        course_title = input("Enter Course Name: ")
        textbook_id = input("Enter Unique ID of the E-textbook: ")
        faculty_id = input("Enter Faculty Member ID: ")
        start_date = input("Enter Course Start Date (YYYY-MM-DD): ")
        end_date = input("Enter Course End Date (YYYY-MM-DD): ")
        course_token = input("Enter Unique Token: ")
        capacity = input("Enter Course Capacity: ")

        print("\n1. Save")
        print("2. Cancel")
        print("3. Landing Page")
        
        choice = input("Enter choice (1-3): ")


        if choice == '1':
            # Validate the inputs (checking for valid IDs in the database)
            
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the Course ID already exists
                cursor.execute("SELECT * FROM Course WHERE course_id = %s", (course_id,))
                existing_course = cursor.fetchone()

                if existing_course:
                    print("A course with this ID already exists. Please try again with a different ID.")
                    continue  # Go back to the input prompt

                # Check if the E-textbook ID exists
                cursor.execute("SELECT * FROM ETextbook WHERE textbook_id = %s", (textbook_id,))
                textbook = cursor.fetchone()

                if not textbook:
                    print("The provided E-textbook ID does not exist. Please enter a valid E-textbook ID.")
                    continue  # Go back to the input prompt

                # Check if the Faculty ID exists
                cursor.execute("SELECT * FROM User WHERE user_id = %s AND role = 'faculty'", (faculty_id,))
                faculty = cursor.fetchone()

                if not faculty:
                    print("The provided Faculty Member ID does not exist or is not assigned to a faculty. Please enter a valid Faculty ID.")
                    continue  # Go back to the input prompt

                # Correctly parse the dates
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

                

                # Insert the new active course into the database
                cursor.execute("""
                    INSERT INTO Course (course_id, title, faculty_id, start_date, end_date, course_type, course_token, capacity, textbook_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (course_id, course_title, faculty_id, start_date, end_date, 'active', course_token, capacity, textbook_id))

                # Commit the changes to the database
                conn.commit()

                # Insert into the Faculty table
                # cursor.execute("""
                #     INSERT INTO Faculty (faculty_id, course_id)
                #     VALUES (%s, %s)
                # """, (faculty_id, course_id))

                # Commit the changes for the Faculty table
                # conn.commit()

                print("New Active Course created successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")

            finally:
                cursor.close()
                conn.close()

            return  # Return to the Admin Landing Page after saving the course

        elif choice == '2':
            print("Cancelling input and returning to the Admin Landing Page...")
            return  # Discard the input and return to Admin Landing Page

        elif choice == '3':
            print("Returning to the Admin Landing Page...")
            return  # Return to Admin Landing Page without saving

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def create_new_eval_course():
    while True:
        print("\n===== Create New Evaluation Course =====")
        course_id = input("Enter Unique Course ID: ")
        course_title = input("Enter Course Name: ")
        textbook_id = input("Enter Unique ID of the E-textbook: ")
        faculty_id = input("Enter Faculty Member ID: ")
        start_date = input("Enter Course Start Date (YYYY-MM-DD): ")
        end_date = input("Enter Course End Date (YYYY-MM-DD): ")
        token = input("Enter Unique Token: ")
        capacity = input("Enter Course Capacity: ")
        

        print("\n1. Save")
        print("2. Cancel")
        print("3. Landing Page")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            # Validate inputs (checking for valid IDs in the database)
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the Course ID already exists
                cursor.execute("SELECT * FROM Course WHERE course_id = %s", (course_id,))
                existing_course = cursor.fetchone()

                if existing_course:
                    print("A course with this ID already exists. Please try again with a different ID.")
                    continue  # Go back to the input prompt

                # Check if the E-textbook ID exists
                cursor.execute("SELECT * FROM ETextbook WHERE textbook_id = %s", (textbook_id,))
                textbook = cursor.fetchone()

                if not textbook:
                    print("The provided E-textbook ID does not exist. Please enter a valid E-textbook ID.")
                    continue  # Go back to the input prompt

                # Check if the Faculty ID exists
                cursor.execute("SELECT * FROM User WHERE user_id = %s AND role = 'faculty'", (faculty_id,))
                faculty = cursor.fetchone()

                if not faculty:
                    print("The provided Faculty Member ID does not exist or is not assigned to a faculty. Please enter a valid Faculty ID.")
                    continue  # Go back to the input prompt

                # Insert the new evaluation course into the database
                cursor.execute("""
                    INSERT INTO Course (course_id, title, faculty_id, start_date, end_date, course_type, course_token, capacity, textbook_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (course_id, course_title, faculty_id, start_date, end_date, 'evaluation', token, capacity, textbook_id))
                conn.commit()

                print("New Evaluation Course created successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return  # Return to the Admin Landing Page after saving the course

        elif choice == '2':
            print("Cancelling input and returning to the Admin Landing Page...")
            return  # Discard the input and return to Admin Landing Page

        elif choice == '3':
            print("Returning to the Admin Landing Page...")
            return  # Return to Admin Landing Page without saving

        else:
            print("Invalid choice. Please select 1, 2, or 3.")



def faculty_login():
    while True:
        print("\n===== Faculty Login =====")
        print("1. Sign-In")
        print("2. Go Back")

        # Take the user's choice
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Proceed with the Sign-In process
            user_id = input("Enter User ID: ")
            password = input("Enter Password: ")

            # Connect to the database and validate the credentials
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT * FROM User WHERE user_id = %s AND password = %s AND role = 'faculty'", (user_id, password))
                user = cursor.fetchone()

                if user:
                    print("Login successful. Welcome Faculty!")
                    faculty_landing(user_id)  # Redirect to faculty home page
                    break  # Exit the loop after successful login
                else:
                    print("Login Incorrect. Please try again.")
            
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard input and go back to the Home page
            print("Returning to the Home page...")
            start_menu()  # Redirects back to the start menu
            break

        else:
            print("Invalid choice. Please enter 1 or 2.")
    

def faculty_landing(faculty_id):
    while True:
        print("Faculty Home: Welcome!")
        print("\n===== Faculty Landing Menu =====")
        print("1. Go to Active Course")
        print("2. Go to Evaluation Course")
        print("3. View Courses")
        print("4. Change Password")
        print("5. Logout")

        # Take input from the faculty
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
            print("Logging out... Returning to the Home page.")
            start_menu()  # Redirect to the Home page or exit the loop
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


def go_to_active_course(faculty_id):
    while True:
        course_id = input("Enter the Active Course ID: ")

        # Validate if the course ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course WHERE course_type = 'active' AND faculty_id = %s AND course_id = %s", (faculty_id, course_id,))
        active_course = cursor.fetchone()
        
        if not active_course:
            print("Invalid Course ID. Please try again.")
            cursor.close()
            conn.close()
            continue
        else:
            cursor.execute("SELECT textbook_id FROM Course WHERE course_id = %s", (course_id,))
            textbook_id = cursor.fetchone()[0]
            # Display Active Course Menu
            print(f"\n===== Active Course Menu (Course ID: {course_id}) =====")
            print("1. View Worklist")
            print("2. Approve Enrollment")
            print("3. View Students")
            print("4. Add New Chapter")
            print("5. Modify Chapters")
            print("6. Add TA")
            print("7. Go Back")

            # Take input from the faculty
            choice = input("Enter choice (1-7): ")

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
                print("Returning to Faculty Landing Page...")
                faculty_landing(faculty_id)  # Redirect back to Faculty Landing Page
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        cursor.close()
        conn.close()


def view_worklist(faculty_id):
    while True:
        try:
            print("\n===== View Worklist =====")
            
            # Connect to the database and retrieve the list of students on the waitlist
            conn = get_db_connection()
            cursor = conn.cursor()

            # Example query to fetch the list of students on the worklist for the faculty's courses
            # You may need to adjust the query based on your actual database structure.
            cursor.execute("""
                SELECT u.user_id, u.first_name, u.last_name, c.title
                FROM User u
                JOIN Enrollment e ON u.user_id = e.student_id
                JOIN Course c ON e.course_id = c.course_id
                WHERE c.faculty_id = %s AND e.status = 'pending' AND u.role = 'student'
            """, (faculty_id,))
            
            worklist = cursor.fetchall()

            if worklist:
                print("\n===== Students in Waiting List =====")
                for student in worklist:
                    print(f"Student ID: {student[0]}, Name: {student[1]} {student[2]}, Course: {student[3]}")
            else:
                print("No students are currently in the waiting list.")

            # Display options to go back to the previous menu
            print("\n1. Go back")
            choice = input("Enter choice: ")

            if choice == '1':
                print("Returning to the Faculty: Active Course page...")
                go_to_active_course(faculty_id)  # Assuming you have a function for the Faculty Active Course page
                break
            else:
                print("Invalid choice. Please select 1.")
        except Exception as msg:
            print(f"An error occurred: {msg}")
            return faculty_landing(faculty_id)
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            return faculty_landing(faculty_id)
        finally:
            cursor.close()
            conn.close()


def approve_enrollment(faculty_id):
    while True:
        print("\n===== Approve Enrollment =====")

        # Get Student ID input from the faculty
        student_id = input("Enter the Student ID: ")

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the student is in the waiting list for a course under the faculty's supervision
        cursor.execute("""
            SELECT e.enrollment_id, c.title
            FROM Enrollment e
            JOIN Course c ON e.course_id = c.course_id
            WHERE e.student_id = %s AND c.faculty_id = %s AND e.status = 'pending'
        """, (student_id, faculty_id))

        enrollment_record = cursor.fetchone()

        if enrollment_record:
            enrollment_id = enrollment_record[0]
            course_name = enrollment_record[1]
            print(f"Student ID {student_id} is waiting for approval in the course: {course_name}")
            
            # Display menu options
            print("\n1. Save (Approve Enrollment)")
            print("2. Cancel")

            choice = input("Enter choice (1-2): ")

            if choice == '1':
                try:
                    # Approve the enrollment by updating the status in the database
                    cursor.execute("""
                        UPDATE Enrollment
                        SET status = 'approved'
                        WHERE enrollment_id = %s
                    """, (enrollment_id,))
                    conn.commit()
                    print(f"Enrollment for Student ID {student_id} in course {course_name} has been approved.")
                except mysql.connector.Error as err:
                    print(f"An error occurred: {err}")
                finally:
                    cursor.close()
                    conn.close()
                return  # Return to the previous page

            elif choice == '2':
                print("Cancelling enrollment approval. Returning to the previous page.")
                cursor.close()
                conn.close()
                return  # Discard input and go back to the previous page
            else:
                print("Invalid choice. Please select 1 or 2.")
        else:
            print(f"No pending enrollment found for Student ID {student_id}. Please try again.")
            cursor.close()
            conn.close()




def view_students(faculty_id):
    while True:
        print("\n===== View Students =====")

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the courses supervised by the faculty
        cursor.execute("""
            SELECT c.course_id, c.title
            FROM Course c
            WHERE c.faculty_id = %s
        """, (faculty_id,))
        courses = cursor.fetchall()

        if courses:
            print("\nCourses supervised by you:")
            for idx, course in enumerate(courses, 1):
                print(f"{idx}. {course[1]} (ID: {course[0]})")

            try:
                # Fetch students enrolled in the selected course
                cursor.execute("""
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
                """, (faculty_id,))
                students = cursor.fetchall()

                if students:
                    print(f"\nStudents enrolled:")
                    for student in students:
                        print(f"Course ID: {student[3]}, ID: {student[0]}, Name: {student[1]} {student[2]}")
                else:
                    print(f"\nNo students found for the course")

            except ValueError:
                print("Invalid input. Please enter a number.")

        else:
            print("You are not supervising any courses.")

        cursor.close()
        conn.close()

        # Display the option to go back
        print("\n1. Go Back")
        choice = input("Enter choice (1): ")

        if choice == '1':
            print("Going back to the previous page.")
            break
        else:
            print("Invalid choice. Please enter 1.")

from datetime import datetime

def add_ta(faculty_id):
    while True:
        print("\n===== Add Teaching Assistant (TA) =====")
        
        # Input TA details
        first_name = input("Enter TA's First Name: ")
        last_name = input("Enter TA's Last Name: ")
        email = input("Enter TA's Email: ")
        default_password = input("Enter a Default Password: ")
        
        # Generate a unique user_id based on TA's name and current date
        user_id_prefix = first_name[:2].upper() + last_name[:2].upper()  # Use uppercase for consistency
        current_date = datetime.now()
        user_id_date = current_date.strftime("%y%m")  # YYMM format
        user_id = user_id_prefix + user_id_date  # Full user_id generation
        print(user_id)
        
        print("\n1. Save")
        print("2. Cancel")
        
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed with saving the TA
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                # Check if email already exists in the database
                cursor.execute("SELECT * FROM User WHERE email=%s", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    print("A user with this email already exists. Please try again with a different email.")
                else:
                    # Insert new TA into the database
                    cursor.execute("""
                        INSERT INTO User (user_id, first_name, last_name, email, password, role)
                        VALUES (%s, %s, %s, %s, %s, 'ta')
                    """, (user_id, first_name, last_name, email, default_password))
                    conn.commit()
                    print("Teaching Assistant added successfully!")
            
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            
            finally:
                cursor.close()
                conn.close()
            
            return  # Return to the previous page after saving TA

        elif choice == '2':
            # Go back to the previous page without saving
            print("Discarding input and going back to the previous page.")
            return  # Go back to the previous page
        
        else:
            print("Invalid choice. Please select 1 or 2.")


def add_new_chapter_faculty(textbook_id, faculty_id):
    while True:
        print("\n===== Add New Chapter =====")
        
        # Input Chapter details
        chapter_id = input("Enter Unique Chapter ID: ")
        chapter_title = input("Enter Chapter Title: ")
        print("\n1. Add New Section")
        print("2. Go Back")
        
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed with saving the new chapter
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                # Check if the Chapter ID already exists
                cursor.execute("SELECT * FROM Chapter WHERE chapter_id=%s", (chapter_id,))
                existing_chapter = cursor.fetchone()

                if existing_chapter:
                    print("A chapter with this ID already exists. Please try again with a different ID.")
                    return add_new_chapter_faculty(textbook_id)
                else:
                    # Insert new chapter into the database
                    cursor.execute("""
                    INSERT INTO Chapter (chapter_id, title, textbook_id)
                    VALUES (%s, %s, %s)
                """, (chapter_id, chapter_title, textbook_id))
                    conn.commit()
                    print("Chapter added successfully!")
                    return add_new_section_faculty(chapter_id, textbook_id, faculty_id)  # Redirect to add new section function
            
            except mysql.connector.Error as err:
                if "chapter_id must be in the format" in str(err):
                    print(f"Error: {err}")
                    print("Please enter a valid chapter_id in the format 'chap[0-9][1-9]'.")
                else:
                    print(f"An error occurred: {err}")
            
            finally:
                cursor.close()
                conn.close()
            
            return  # Return to the previous page after saving the chapter

        elif choice == '2':
            # Go back to the previous page without saving
            print("Discarding input and going back to the previous page.")
            return faculty_landing(faculty_id) # Go back to the previous page
        
        else:
            print("Invalid choice. Please select 1 or 2.")


def modify_chapter_faculty(textbook_id, faculty_id):
    while True:
        print("\n===== Modify Chapter =====")

        # Input the unique Chapter ID
        chapter_id = input("Enter Unique Chapter ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s", (chapter_id,textbook_id))
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
            hide_chapter(chapter_id,textbook_id)
        elif choice == '2':
            delete_chapter(chapter_id,textbook_id)
        elif choice == '3':
            add_new_section_faculty(chapter_id,textbook_id, faculty_id)
        elif choice == '4':
            modify_section_faculty(chapter_id,textbook_id, faculty_id)
        elif choice == '5':
            print("Going back to the previous page...")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")
        
        cursor.close()
        conn.close()

def hide_chapter(chapter_id, textbook_id):
    while True:
        print("\n===== Hide Chapter =====")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Call the hide_chapter stored procedure
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('hide_chapter', [chapter_id, textbook_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])  # Print the success or error message
            except mysql.connector.Error as err:
                print(f"Failed: An error occurred - {err}")
            finally:
                cursor.close()
                conn.close()
            break  # Exit the loop after performing the action
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break  # Exit the loop without performing any action
        else:
            print("Invalid choice. Please enter 1 or 2.")


def delete_chapter(chapter_id, textbook_id):
    while True:
        print("\n===== Delete Chapter =====")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Call the delete_chapter stored procedure
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('delete_chapter', [chapter_id, textbook_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])  # Print the success or error message
            except mysql.connector.Error as err:
                print(f"Failed: An error occurred - {err}")
            finally:
                cursor.close()
                conn.close()
            break  # Exit the loop after performing the action
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break  # Exit the loop without performing any action
        else:
            print("Invalid choice. Please enter 1 or 2.")

def add_new_section_faculty(chapter_id, textbook_id, faculty_id):
    while True:
        print("\n===== Add New Section =====")
        section_number = input("Enter Section Number: ")
        section_title = input("Enter Section Title: ")

        print("\n1. Add New Content Block")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to add a new content block for the created section
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the section already exists
                cursor.execute("SELECT * FROM Section WHERE section_number=%s AND chapter_id=%s AND textbook_id = %s", (section_number, chapter_id, textbook_id))
                existing_section = cursor.fetchone()

                if existing_section:
                    print(f"A section with number {section_number} already exists for this chapter.")
                    return add_new_section_faculty(chapter_id, textbook_id, faculty_id)
                else:
                    # Insert the new section into the database with the correct column name
                    cursor.execute("""
                        INSERT INTO Section (section_number, title, chapter_id,textbook_id)
                        VALUES (%s, %s, %s, %s)
                    """, (section_number, section_title, chapter_id,textbook_id))
                    conn.commit()
                    print("Section created successfully! Redirecting to Add New Content Block...")
                    cursor.execute("SELECT section_id FROM Section WHERE chapter_id = %s AND textbook_id = %s AND section_number = %s", (chapter_id, textbook_id, section_number))
                    section_id = cursor.fetchone()[0]
                    return add_new_content_block_faculty(section_id, faculty_id)  # Redirect to add new content block
            except mysql.connector.Error as err:
                if "section_number must be in the format" in str(err):
                    print(f"Error: {err}")
                    print("Please enter a valid section_number in the format 'sec[0-9][1-9]'.")
                else:
                        print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Go back to the previous page without saving
            print("Discarding input. Returning to the previous page...")
            return add_new_chapter_faculty(textbook_id, faculty_id) # Return to the previous page
        else:
            print("Invalid choice. Please select 1 or 2.")

def modify_section_faculty(chapter_id,textbook_id, faculty_id):
    while True:
        print("\n===== Modify Section =====")
        section_number = input("Enter Section Number: ")

        # Check if the section exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT section_id FROM Section
                WHERE section_number = %s AND chapter_id = %s AND textbook_id = %s
            """, (section_number, chapter_id, textbook_id))

            section_id = cursor.fetchone()[0]

            if not section_id:
                print(f"Section {section_number} does not exist. Please try again.")
                cursor.close()
                conn.close()
                return  # Return if the section does not exist

            # Display the menu for modification options
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
        print("\n===== Hide Section =====")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Call the hide_section stored procedure
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('hide_section', [section_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])  # Print the success or error message
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            break  # Exit after action is performed
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break  # Exit without any action
        else:
            print("Invalid choice. Please enter 1 or 2.")


def delete_section(section_id):
    while True:
        print("\n===== Delete Section =====")
        print("1. Save")
        print("2. Cancel")

        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Call the delete_section stored procedure
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.callproc('delete_section', [section_id])
                for result in cursor.stored_results():
                    print(result.fetchone()[0])  # Print the success or error message
            except mysql.connector.Error as err:
                print(f"Failure. An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            break  # Exit after action is performed
        elif choice == '2':
            print("Cancelled: Returning to the previous page.")
            break  # Exit without any action
        else:
            print("Invalid choice. Please enter 1 or 2.")


def add_new_content_block_faculty(section_id, faculty_id):
    while True:
        print(f"\n===== Add New Content Block for Section (ID: {section_id}) =====")
        
        # Input Content Block ID
        content_block_id = input("Enter Unique Content Block ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO ContentBlock (content_block_id, section_id) VALUES (%s, %s)", (content_block_id, section_id,))
            conn.commit()
        except mysql.connector.Error as err:
            if "content_block_id must be in the format" in str(err):
                print(f"Error: {err}")
                print("Please enter a valid Content Block ID the format 'sec[0-9][1-9]'.")
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
            return add_text_faculty(content_block_id, section_id, faculty_id)  # Pass section_id to add_text_faculty

        elif choice == '2':
            return add_picture_faculty(content_block_id, section_id, faculty_id)  # Pass section_id to add_picture_faculty

        elif choice == '3':
            return add_activity_faculty(content_block_id, section_id, faculty_id)  # Pass section_id to add_activity_faculty

        elif choice == '4':
            # Go back to the previous menu
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT chapter_id, textbook_id FROM Section WHERE section_id = %s", (section_id,))
            result = cursor.fetchone()
            chapter_id, textbook_id = result
            print("Going back to the previous page...")
            return add_new_section_faculty(chapter_id, textbook_id, faculty_id)
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


def modify_content_block_faculty(section_id, faculty_id):
    while True:
        print("\n===== Modify Content Block =====")
        
        # Input Content Block ID
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
            hide_content_block_faculty(section_id, content_block_id)  # Hide content block
            return

        elif choice == '2':
            delete_content_block_faculty(section_id, content_block_id)  # Delete content block
            return

        elif choice == '3':
            add_text_faculty(content_block_id, section_id, faculty_id)  # Add text to content block
            return

        elif choice == '4':
            add_picture_faculty(content_block_id, section_id, faculty_id)  # Add picture to content block
            return

        elif choice == '5':
            hide_activity_faculty(section_id, content_block_id)  # Hide activity
            return

        elif choice == '6':
            delete_activity_faculty(section_id, content_block_id)  # Delete activity
            return

        elif choice == '7':
            add_activity_faculty(content_block_id, section_id, faculty_id)  # Add activity
            return

        elif choice == '8':
            # Go back to the previous page
            print("Going back to the previous page...")
            return

        else:
            print("Invalid choice. Please select a number between 1 and 8.")


def hide_content_block_faculty(section_id, content_block_id):
    while True:
        print("\n===== Hide Content Block =====")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to hide the content block
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if content block exists
                # cursor.execute("SELECT * FROM ContentBlock WHERE content_block_id = %s", (content_block_id,))
                # content_block = cursor.fetchall()

                cursor.execute("""
                    UPDATE ContentBlock
                    SET hidden = 'yes'
                    WHERE content_block_id = %s
                    AND section_id = %s
                """, (content_block_id, section_id))
                conn.commit()
                print("Content Block hidden successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard the input and go back
            print("Discarding input and going back to the previous menu...")
            return
        else:
            print("Invalid choice. Please select 1 or 2.")

def delete_content_block_faculty(section_id, content_block_id):
    while True:
        print("\n===== Delete Content Block =====")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to delete the content block
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("DELETE FROM ContentBlock WHERE content_block_id = %s AND section_id=%s", (content_block_id, section_id))
                conn.commit()
                print("Content Block deleted successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard the input and go back
            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

def hide_activity_faculty(section_id, content_block_id):
    while True:
        print("\n===== Hide Activity =====")
        
        # Input the unique activity ID
        activity_id = input("Enter the unique Activity ID: ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to hide the activity
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the activity exists
                cursor.execute("SELECT * FROM Activity WHERE activity_id=%s AND section_id = %s AND content_block_id = %s", (activity_id, section_id, content_block_id,))
                activity = cursor.fetchone()

                if activity:
                    # Update the activity status to 'hidden'
                    cursor.execute("""
                        UPDATE Activity
                        SET hidden = 'yes'
                        WHERE activity_id = %s AND section_id = %s AND content_block_id = %s
                    """, (activity_id, section_id, content_block_id))
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
            # Discard input and go back to the previous page
            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

def delete_activity_faculty(section_id, content_block_id):
    while True:
        print("\n===== Delete Activity =====")
        
        # Input the unique activity ID
        activity_id = input("Enter the unique Activity ID: ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to delete the activity
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the activity exists
                cursor.execute("SELECT * FROM Activity WHERE activity_id=%s AND section_id = %s AND content_block_id = %s", (activity_id, section_id, content_block_id,))
                activity = cursor.fetchone()

                if activity:
                    # Delete the activity from the database
                    cursor.execute("DELETE FROM Activity WHERE activity_id = %s AND section_id = %s AND content_block_id = %s", (activity_id, section_id, content_block_id,))
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
            # Discard input and go back to the previous page
            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

def add_text_faculty(content_block_id, section_id, faculty_id):
    while True:
        print("\n===== Add Text to Content Block =====")
        
        # Input the text
        text_content = input("Enter the text: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to add text to the content block
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s", ('text', text_content, content_block_id, section_id))
                conn.commit()
                print(f"Text content added to Content Block {content_block_id} successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard input and go back to the previous page
            print("Discarding input and going back to the previous menu...")
            return add_new_content_block_faculty(section_id, faculty_id)

        else:
            print("Invalid choice. Please select 1 or 2.")

def add_picture_faculty(content_block_id, section_id, faculty_id):
    while True:
        print("\n===== Add Picture to Content Block =====")
        
        # Input the picture file path (this could be a path or URL, depending on implementation)
        picture_content = input("Enter the picture file path or URL: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to add picture to the content block
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Insert the picture into the ContentBlock table
                cursor.execute("UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s", ('picture', picture_content, content_block_id, section_id))
                conn.commit()
                print("Picture added successfully!")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard input and go back to the previous page
            print("Discarding input and going back to the previous menu...")
            return add_new_content_block_faculty(section_id, faculty_id)

        else:
            print("Invalid choice. Please select 1 or 2.")

def add_activity_faculty(content_block_id, section_id, faculty_id):
    while True:
        print("\n===== Add Activity =====")
        
        activity_id = input("Enter Unique Activity ID: ")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Activity (activity_id, content_block_id, section_id)
                VALUES (%s, %s, %s)
            """, (activity_id, content_block_id, section_id,))
            conn.commit()
            print(f"Activity with ID {activity_id} added successfully to Content Block {content_block_id}.")
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

        print("\n1. Add Question")
        print("2. Go Back")

        choice = input("Enter choice (1-2): ")

        if choice == '1':
            add_question_faculty(activity_id, content_block_id, section_id, faculty_id)  # Add questions to this activity
            return  # Return to previous page after adding the question

        elif choice == '2':
            print("Discarding input. Returning to the previous page...")
            return add_new_content_block_faculty(section_id, faculty_id) # Return to the previous page
        
        else:
            print("Invalid choice. Please select 1 or 2")

        ###################################

        # # Input the unique activity ID
        # activity_id = input("Enter the unique Activity ID: ")

        # print("\n1. Add Question")
        # print("2. Go Back")
        # choice = input("Enter choice (1-2): ")

        # if choice == '1':
        #     # Proceed to add questions for the activity
        #     conn = get_db_connection()
        #     cursor = conn.cursor()

        #     try:
        #         # Check if the activity ID already exists
        #         cursor.execute("SELECT * FROM Activity WHERE activity_id=%s", (activity_id,))
        #         existing_activity = cursor.fetchone()

        #         if existing_activity:
        #             print("An activity with this ID already exists. Please try again with a different ID.")
        #         else:
        #             # Insert the new activity into the database
        #             cursor.execute("""
        #                 INSERT INTO Activity (activity_id, content_block_id)
        #                 VALUES (%s, %s)
        #             """, (activity_id, content_block_id))
        #             conn.commit()
        #             print("Activity created successfully!")
        #             add_question_faculty(activity_id)  # Redirect to add question function
        #             return  # Return after adding question

        #     except mysql.connector.Error as err:
        #         print(f"An error occurred: {err}")
        #     finally:
        #         cursor.close()
        #         conn.close()

        # elif choice == '2':
        #     # Discard input and go back to the previous page
        #     print("Discarding input and going back to the previous menu...")
        #     return

        # else:
        #     print("Invalid choice. Please select 1 or 2.")

# def add_question_faculty(activity_id):
#     while True:
#         print("\n===== Add Question =====")
        
#         # Input the question details
#         question_id = input("Enter Question ID: ")
#         question_text = input("Enter Question Text: ")
#         opt1 = input("Enter Option 1: ")
#         opt1_exp = input("Enter Explanation for Option 1: ")
#         opt2 = input("Enter Option 2: ")
#         opt2_exp = input("Enter Explanation for Option 2: ")
#         opt3 = input("Enter Option 3: ")
#         opt3_exp = input("Enter Explanation for Option 3: ")
#         opt4 = input("Enter Option 4: ")
#         opt4_exp = input("Enter Explanation for Option 4: ")
#         correct_answer = input("Enter the Correct Answer (Option 1/2/3/4): ")

#         print("\n1. Save")
#         print("2. Cancel")
#         choice = input("Enter choice (1-2): ")

#         if choice == '1':
#             # Save the question to the database
#             conn = get_db_connection()
#             cursor = conn.cursor()

#             try:
#                 # Check if the question ID already exists
#                 cursor.execute("SELECT * FROM Question WHERE question_id=%s", (question_id,))
#                 existing_question = cursor.fetchone()

#                 if existing_question:
#                     print("A question with this ID already exists. Please try again with a different ID.")
#                 else:
#                     # Insert the new question into the database
#                     cursor.execute("""
#                         INSERT INTO Question (question_id, question_text, option1, option1_exp, option2, option2_exp, 
#                                               option3, option3_exp, option4, option4_exp, correct_answer, activity_id)
#                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """, (question_id, question_text, opt1, opt1_exp, opt2, opt2_exp, opt3, opt3_exp, opt4, opt4_exp, correct_answer, activity_id))
#                     conn.commit()
#                     print("Question saved successfully!")
#                     return  # Go back to the previous page

#             except mysql.connector.Error as err:
#                 print(f"An error occurred: {err}")
#             finally:
#                 cursor.close()
#                 conn.close()

#         elif choice == '2':
#             # Discard input and go back to the previous page
#             print("Discarding input and going back to the previous menu...")
#             return

#         else:
#             print("Invalid choice. Please select 1 or 2.")


def go_to_evaluation_course(faculty_id):
    while True:
        course_id = input("Enter the Evaluation Course ID: ")

        # Validate if the course ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Course WHERE course_type = 'evaluation' AND faculty_id = faculty_id AND course_id = %s", (course_id,))
        evaluation_course = cursor.fetchone()

        if not evaluation_course:
            print("Invalid Course ID. Please try again.")
            cursor.close()
            conn.close()
            continue
        else:
            # Display Evaluation Course Menu
            cursor.execute("SELECT textbook_id FROM Course WHERE course_id = %s", (course_id,))
            textbook_id = cursor.fetchone()[0]
            print(f"\n===== Evaluation Course Menu (Course ID: {course_id}) =====")
            print("1. Add New Chapter")
            print("2. Modify Chapters")
            print("3. Go Back")

            # Take input from the faculty
            choice = input("Enter choice (1-3): ")

            if choice == '1':
                add_new_chapter_faculty(textbook_id, faculty_id)
            elif choice == '2':
                modify_chapter_faculty(textbook_id, faculty_id)
            elif choice == '3':
                print("Returning to Faculty Landing Page...")
                faculty_landing(faculty_id)  # Redirect back to Faculty Landing Page
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

        cursor.close()
        conn.close()

def view_courses(faculty_id):
    while True:
        print(f"\n===== Assigned Courses for Faculty ID: {faculty_id} =====")

        # Connect to the database and retrieve courses assigned to the faculty member
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get the courses assigned to the faculty
        cursor.execute("SELECT course_id, title FROM Course WHERE faculty_id = %s", (faculty_id,))
        assigned_courses = cursor.fetchall()

        if not assigned_courses:
            print("No courses assigned.")
        else:
            print("Assigned Courses:")
            for course in assigned_courses:
                print(f"Course ID: {course[0]}, Course Name: {course[1]}")

        # Display the option to go back
        print("\n1. Go Back")
        choice = input("Enter choice (1 to Go Back): ")

        if choice == '1':
            print("Returning to Faculty Landing Page...")
            faculty_landing(faculty_id)  # Redirect back to Faculty Landing Page
            break
        else:
            print("Invalid choice. Please select 1 to go back.")

        cursor.close()
        conn.close()




def change_password(faculty_id):
    while True:
        print("\n===== Change Password =====")
        
        # Input fields
        current_password = input("Enter Current Password: ")
        new_password = input("Enter New Password: ")
        confirm_password = input("Confirm New Password: ")

        # Connect to the database to validate the current password
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the current password matches the one in the database
        cursor.execute("SELECT password FROM User WHERE user_id = %s AND role = 'faculty'", (faculty_id,))
        result = cursor.fetchone()

        if result:
            db_password = result[0]
            if db_password != current_password:
                print("Current password is incorrect. Please try again.")
            elif new_password != confirm_password:
                print("New passwords do not match. Please try again.")
            else:
                # Update the password in the database
                cursor.execute("UPDATE User SET password = %s WHERE user_id = %s AND role = 'faculty'", (new_password, faculty_id))
                conn.commit()
                print("Password updated successfully!")
                break
        else:
            print("User not found or password mismatch.")

        cursor.close()
        conn.close()

        # Display options after handling the password update
        print("\n1. Update Again")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            continue  # Re-run the password update logic
        elif choice == '2':
            print("Returning to Faculty Landing Page...")
            faculty_landing()  # Redirect back to Faculty Landing Page
            break
        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_login():
    while True:
        print("\n===== TA Login =====")
        
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")

        print("\n1. Sign-In")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Validate the credentials
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check the TA's login credentials in the database
                cursor.execute("SELECT * FROM User WHERE user_id=%s AND password=%s AND role=%s", (user_id, password, 'ta'))
                ta_user = cursor.fetchone()

                if ta_user:
                    print("Login successful. Redirecting to TA Landing Page...")
                    ta_id = ta_user[0]  # Assuming the first column in User table is user_id which is ta_id
                    ta_landing_page(ta_id)  # Pass ta_id to the landing page
                else:
                    print("Login Incorrect. Please check your credentials and try again.")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard the input and go back to the home page
            print("Going back to the Home page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

# Modify the TA landing page to accept ta_id
def ta_landing_page(ta_id):
    while True:
        print("\n===== TA Landing Page =====")
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
            return start_menu() # You can redirect to the main menu or home page function here
        else:
            print("Invalid choice. Please select a number between 1 and 4.")


def ta_go_to_active_course(ta_id):
    while True:

        course_id = input("Enter the Active Course ID: ")

        # Validate if the course ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT c.textbook_id FROM Course c JOIN TeachingAssistant t ON t.course_id = c.course_id WHERE c.course_type = 'active' AND t.teaching_assistant_id = %s AND c.course_id = %s", (ta_id, course_id,))
        textbook_id = cursor.fetchone()[0]

        print("\n===== TA: Active Course Menu =====")
        print("1. View Students")
        print("2. Add New Chapter")
        print("3. Modify Chapters")
        print("4. Go Back")

        choice = input("Enter choice (1-4): ")

        if choice == '1':
            # Redirect to view students (implement function for this)
            ta_view_students(ta_id)
        elif choice == '2':
            # Redirect to add a new chapter (implement function for this)
            ta_add_new_chapter(ta_id, textbook_id)
        elif choice == '3':
            # Redirect to modify chapters (implement function for this)
            ta_modify_chapter(textbook_id, ta_id)
        elif choice == '4':
            # Go back to the previous menu
            print("Going back to the previous page...")
            return
        else:
            print("Invalid choice. Please select a number between 1 and 4.")

def ta_view_courses(ta_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Retrieve assigned courses from the database for the specified TA
        cursor.execute("SELECT t.course_id, c.title FROM TeachingAssistant t JOIN Course c ON c.course_id = t.course_id WHERE t.teaching_assistant_id = %s", (ta_id,))
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
            # Here, you'd typically call a function that brings the user back to the TA landing page
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
        print("\n===== Change Password =====")
        current_password = input("Enter current password: ")
        new_password = input("Enter new password: ")
        confirm_new_password = input("Confirm new password: ")

        print("\n1. Update")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            if new_password != confirm_new_password:
                print("New passwords do not match. Please try again.")
                continue  # Restart the loop if the new passwords don't match

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # First verify the current password
                cursor.execute("SELECT password FROM User WHERE user_id=%s AND role='ta'", (ta_id,))
                actual_current_password = cursor.fetchone()[0]

                if actual_current_password == current_password:
                    # Update the password if the current password is correct
                    cursor.execute("UPDATE User SET password=%s WHERE user_id=%s AND role='ta'", (new_password, ta_id))
                    conn.commit()
                    print("Password updated successfully!")
                else:
                    print("Current password is incorrect. Please try again.")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

            break  # Exit the loop after attempt to update password

        elif choice == '2':
            print("Cancelling and going back to the previous page...")
            break  # Exit the loop and do not update the password

        else:
            print("Invalid choice. Please select 1 or 2.")


def ta_view_students(ta_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetching courses the TA is linked to
        cursor.execute("SELECT course_id FROM TeachingAssistant WHERE teaching_assistant_id=%s", (ta_id,))
        courses = cursor.fetchall()
        if not courses:
            print("You are not assigned to any courses.")
            return

        # Fetching students from these courses
        for course in courses:
            course_id = course[0]
            print(f"\nStudents in Course ID {course_id}:")
            cursor.execute("""
                SELECT DISTINCT e.student_id, CONCAT(u.first_name, " ", u.last_name) as name, e.status
                FROM Enrollment e
                JOIN User u ON u.user_id = e.student_id
                WHERE course_id=%s
            """, (course_id,))
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
            # Here, you'd typically call a function that brings the user back to the TA landing page
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
    print("\n===== Add New Chapter =====")
    chapter_id = input("Enter Unique Chapter ID: ")
    chapter_title = input("Enter Chapter Title: ")

    # Connect to the database and attempt to add the chapter
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert the new chapter into the database
        cursor.execute("INSERT INTO Chapter(chapter_id, title, textbook_id) VALUES (%s, %s, %s)", (chapter_id, chapter_title, textbook_id))
        conn.commit()
        print("Chapter added successfully.")

        while True:
            print("\n1. Add New Section")
            print("2. Go Back")
            choice = input("Choose an option (1-2): ")

            if choice == '1':
                ta_add_new_section(chapter_id, textbook_id, ta_id)  # Navigate to the function to add a new section
                # break  # Break the loop after adding the section
            elif choice == '2':
                print("Returning to the previous menu...")
                return ta_go_to_active_course(ta_id)  # Exit the function to return to the previous menu
            else:
                print("Invalid choice. Please select either 1 or 2.")

    except mysql.connector.Error as err:
        if "chapter_id must be in the format" in str(err):
            print(f"Error: {err}")
            print("Please enter a valid chapter_id in the format 'chap[0-9][1-9]'.")
        else:
            print(f"An error occurred: {err}")
            conn.rollback()  # Rollback in case of any error during the insert

    finally:
        cursor.close()
        conn.close()

def ta_add_new_section(chapter_id, textbook_id, ta_id):
    print("\n===== Add New Section =====")
    section_number = input("Enter Section Number: ")
    section_title = input("Enter Section Title: ")

    # Establish a database connection to check if the section already exists
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the section already exists in the database
        cursor.execute("SELECT * FROM Section WHERE section_number=%s AND chapter_id=%s AND textbook_id = %s", (section_number, chapter_id, textbook_id))
        if cursor.fetchone():
            print("Section already exists with this number. Please try another section number.")
            return ta_add_new_section(chapter_id, textbook_id, ta_id)
        else:
            # Section does not exist, proceed to add
            print("\n1. Add New Content Block")
            print("2. Go Back")
            choice = input("Choose an option (1-2): ")

            if choice == '1':
                # Function to add a new content block
                cursor.execute("""
                    INSERT INTO Section (section_number, title, chapter_id,textbook_id)
                    VALUES (%s, %s, %s, %s)
                """, (section_number, section_title, chapter_id,textbook_id))
                conn.commit()
                print("Section created successfully! Redirecting to Add New Content Block...")
                cursor.execute("SELECT section_id FROM Section WHERE chapter_id = %s AND textbook_id = %s AND section_number = %s", (chapter_id, textbook_id, section_number))
                section_id = cursor.fetchone()[0]
                return ta_add_new_content_block(chapter_id, section_id, ta_id, textbook_id)
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
    print("\n===== Modify Chapter =====")
    chapter_id = input("Enter Unique Chapter ID: ")

    # Establish a database connection to validate the chapter ID
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the chapter ID exists in the database
        cursor.execute("SELECT * FROM Chapter WHERE chapter_id = %s AND textbook_id = %s", (chapter_id,textbook_id))
        chapter = cursor.fetchone()[0]
        if not chapter:
            print("The chapter ID does not exist. Please enter a valid Chapter ID.")
            return  # Exit if the chapter ID is not found
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
        return  # Exit on error
    finally:
        cursor.close()
        conn.close()

    while True:
        print("\n1. Add New Section")
        print("2. Modify Section")
        print("3. Go Back")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            ta_add_new_section(chapter_id, textbook_id, ta_id)  # Function to add a new section
        elif choice == '2':
            ta_modify_section(chapter_id, textbook_id, ta_id)  # Function to add a new activity
        elif choice == '3':
            print("Returning to the previous menu...")
            break  # Exit the function to return to the previous menu
        else:
            print("Invalid choice. Please select either 1, 2, or 3.")

def ta_add_new_content_block(chapter_id, section_id, ta_id, textbook_id):
    while True:
        print("\n===== Add New Content Block =====")
        content_block_id = input("Enter Content Block ID: ")
        
        # Database check for existing content block ID
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s", (content_block_id,))
            (count,) = cursor.fetchone()
            if count > 0:
                print("A content block with this ID already exists. Please try a different ID.")
                continue
            else:
                cursor.execute("INSERT INTO ContentBlock (content_block_id, section_id) VALUES (%s, %s)", (content_block_id, section_id,))
                conn.commit()
        except mysql.connector.Error as err:
            if "content_block_id must be in the format" in str(err):
                print(f"Error: {err}")
                print("Please enter a valid Content Block ID the format 'sec[0-9][1-9]'.")
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
        print("\n===== Hide Activity =====")
        
        # Input the unique activity ID
        activity_id = input("Enter the unique Activity ID: ")

        print("\n1. Save")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Proceed to hide the activity
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the activity exists
                cursor.execute("SELECT * FROM Activity WHERE activity_id=%s AND section_id = %s AND content_block_id = %s", (activity_id, section_id, content_block_id,))
                activity = cursor.fetchone()

                if activity:
                    # Update the activity status to 'hidden'
                    cursor.execute("""
                        UPDATE Activity
                        SET hidden = 'yes'
                        WHERE activity_id = %s AND section_id = %s AND content_block_id = %s
                    """, (activity_id, section_id, content_block_id))
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
            # Discard input and go back to the previous page
            print("Discarding input and going back to the previous menu...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

def ta_add_text(content_block_id, section_id):
    while True:
        print("\n===== Add Text to Content Block =====")
        text_input = input("Enter the text to add: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Save the text to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Insert the text into the ContentBlock table
                cursor.execute("UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s", ('text', text_input, content_block_id, section_id))
                conn.commit()
                print("Text has been added successfully to the content block.")
                return  # Return to the previous page after successful save
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard the input and go back to the previous page
            print("Going back to the previous page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

def ta_add_picture(content_block_id, section_id):
    while True:
        print("\n===== Add Picture to Content Block =====")
        
        picture_path = input("Enter the file path or URL of the picture: ")

        print("\n1. Add")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Save the picture to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Insert the picture details into the ContentBlocks table
                cursor.execute("UPDATE ContentBlock SET block_type = %s, content = %s WHERE content_block_id = %s AND section_id = %s", ('picture', picture_path, content_block_id, section_id))
                conn.commit()
                print("Picture has been added successfully to the content block.")
                return  # Go back to the previous page after successful save
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard the input and go back to the previous page
            print("Going back to the previous page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")

def ta_add_new_activity(content_block_id, section_id):
    while True:
        print("\n===== Add Activity =====")
        
        activity_id = input("Enter the Unique Activity ID: ")

        # Check if the Activity ID exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Query to check if the activity ID exists in the database
            cursor.execute("""
                INSERT INTO Activity (activity_id, content_block_id, section_id)
                VALUES (%s, %s, %s)
            """, (activity_id, content_block_id, section_id,))
            conn.commit()
            print(f"Activity with ID {activity_id} added successfully to Content Block {content_block_id}.")

        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        # Present menu options
        print("\n1. Add Question")
        print("2. Go Back")
        choice = input("Enter choice (1-2): ")

        if choice == '1':
            # Redirect to the Add Question page
            print(f"Redirecting to Add Question page for Activity ID: {activity_id}...")
            ta_add_question(activity_id, content_block_id, section_id)
            return  # After adding the question, return to the previous page
        elif choice == '2':
            # Discard the input and go back to the previous page
            print("Going back to the previous page...")
            return
        else:
            print("Invalid choice. Please select 1 or 2.")

def ta_add_question(activity_id, content_block_id, section_id):
    while True:
        print("\n===== Add Question =====")

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
            # Insert the question into the Activity table
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO Question (question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option, activity_id, section_id, content_block_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (question_id, question_text, option1_text, option2_text, option3_text, option4_text, option1_explanation, option2_explanation, option3_explanation, option4_explanation, correct_option, activity_id, section_id, content_block_id))
                conn.commit()
                print("Question and options added successfully!")
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()
            return ta_add_new_activity(content_block_id, section_id) # Go back to the previous menu after saving

        elif choice == '2':
            print("Discarding input. Returning to Add Activity page...")
            return ta_add_new_activity(content_block_id, section_id) # Return to Add Activity page
        else:
            print("Invalid choice. Please select 1 or 2.")

def ta_modify_section(chapter_id, textbook_id, ta_id):
    while True:
        print("\n===== Modify Section =====")
        
        # Take input for section details
        section_number = input("Enter Section Number: ")

        # Database check to see if section exists
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT section_id FROM Section
                WHERE section_number = %s AND chapter_id = %s AND textbook_id = %s
            """, (section_number, chapter_id, textbook_id))
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
            # Call your function to add a new content block, passing the relevant details
            ta_add_new_content_block(chapter_id, section_id, ta_id, textbook_id)

        elif choice == '2':
            print("Modifying content block...")
            # Call your function to modify a content block, passing relevant details
            ta_modify_content_block(section_id,ta_id)

        elif choice == '3':
            print("Deleting content block...")
            # Call your function to delete a content block
            ta_delete_content_block(section_id)

        elif choice == '4':
            print("Hiding content block...")
            # Call your function to hide a content block
            ta_hide_content_block(section_id)

        elif choice == '5':
            print("Going back to the previous page...")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 5.")

def ta_modify_content_block(section_id, ta_id):
    while True:
        print("\n===== Modify Content Block =====")
        
        # Input for Content Block ID
        content_block_id = input("Enter Content Block ID: ")

        # Database check to see if content block exists
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s AND section_id = %s", (content_block_id, section_id,))
            (count,) = cursor.fetchone()
            if count == 0:
                print("This content block does not exist. Please check the details or create a new content block.")
                continue
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        # Menu for modifying content block
        print("\n1. Add Text")
        print("2. Add Picture")
        print("3. Add Activity")
        print("4. Go Back")
        print("5. Landing Page")
        
        choice = input("Enter choice (1-5): ")

        if choice == '1':
            print("Adding Text...")
            # Call your function to add text
            ta_add_text(content_block_id, section_id)

        elif choice == '2':
            print("Adding Picture...")
            # Call your function to add a picture
            ta_add_picture(content_block_id, section_id)

        elif choice == '3':
            print("Adding Activity...")
            # Call your function to add an activity
            ta_add_new_activity(content_block_id, section_id)

        elif choice == '4':
            print("Going back to the previous page...")
            break

        elif choice == '5':
            print("Redirecting to User Landing Page...")
            # Call the landing page function here
            ta_landing_page()
            break

        else:
            print("Invalid choice. Please select a number between 1 and 5.")

def ta_delete_content_block(section_id):
    while True:
        print("\n===== Delete Content Block =====")
        
        # Input for Content Block ID
        content_block_id = input("Enter Content Block ID: ")

        # Database check to see if content block exists
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s AND section_id = %s", (content_block_id, section_id,))
            (count,) = cursor.fetchone()
            if count == 0:
                print("This content block does not exist. Please check the ID or go back.")
                continue
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        # Menu for deleting or going back
        print("\n1. Delete")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Delete content block from the database
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM ContentBlock WHERE content_block_id = %s AND section_id = %s", (content_block_id, section_id,))
                conn.commit()
                print(f"Content Block with ID {content_block_id} has been deleted successfully.")
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
        print("\n===== Hide Content Block =====")
        
        # Input for Content Block ID
        content_block_id = input("Enter Content Block ID: ")

        # Database check to see if content block exists
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM ContentBlock WHERE content_block_id = %s AND section_id = %s", (content_block_id, section_id,))
            (count,) = cursor.fetchone()
            if count == 0:
                print("This content block does not exist. Please check the ID or go back.")
                continue
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            continue
        finally:
            cursor.close()
            conn.close()

        # Menu for hiding or going back
        print("\n1. Hide")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Hide the content block in the database (using a 'hidden' flag or similar)
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE ContentBlock SET hidden = 'yes' WHERE content_block_id = %s and section_id = %s", (content_block_id, section_id))
                conn.commit()
                print(f"Content Block with ID {content_block_id} has been hidden successfully.")
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
        print("\n===== Student Login Menu =====")
        print("1. Enroll in a Course")
        print("2. Sign-In")
        print("3. Go Back")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            # Redirect to the enrollment process (implement the enrollment function)
            enroll_in_course()
        elif choice == '2':
            # Redirect to the sign-in process (implement the sign-in function)
            student_sign_in()
        elif choice == '3':
            # Go back to the previous page
            print("Going back to the Home page...")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 3.")

def enroll_in_course():
    while True:
        print("\n===== Student Enrollment =====")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        email = input("Enter Email: ")
        course_token = input("Enter Course Token: ")

        print("\n1. Enroll")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Proceed with the enrollment process
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Check if the student is already enrolled in the system
                cursor.execute("SELECT user_id FROM User WHERE email=%s AND role = 'student'", (email,))
                student_id = cursor.fetchone()
                
                cursor.execute("SELECT course_id FROM Course WHERE course_token=%s AND course_type = 'active'", (course_token,))
                course_id = cursor.fetchone()
                
                if not course_id:
                    print(f"Invalid course token.")
                    continue
                
                course_id = course_id[0]

                if student_id:
                    # Student exists, just enroll them in the course
                    student_id = student_id[0]
                    print(f"Student already exists. Adding to course with token {course_token}.")
                    cursor.execute("INSERT INTO Enrollment (student_id, course_id, status) VALUES (%s, %s, %s)", 
                                   (student_id, course_id, 'pending'))
                else:
                    # Student doesn't exist, create a new student entry and enroll them
                    print(f"Creating a new student and adding to course with token {course_token}.")
                    user_id_prefix = first_name[:2] + last_name[:2]
                    current_date = datetime.now()
                    user_id_date = current_date.strftime("%y%m")
                    student_id = user_id_prefix + user_id_date
                    print(f"Generated User ID: {student_id}")
                    cursor.execute("INSERT INTO User (user_id, first_name, last_name, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)", 
                                   (student_id, first_name, last_name, email, 'defaultpassword', 'student'))
                    cursor.execute("INSERT INTO Student (student_id) VALUES (%s)", 
                                   (student_id,))
                    cursor.execute("INSERT INTO Enrollment (student_id, course_id, status) VALUES (%s, %s, %s)", 
                                   (student_id, course_id, 'pending'))

                conn.commit()
                print(f"Enrollment request submitted. You have been added to the waiting list for course {course_token}.")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Go back to the previous page (Login menu)
            print("Going back to the Login page...")
            break

        else:
            print("Invalid choice. Please select 1 or 2.")


def student_sign_in():
    while True:
        print("\n===== Student Sign-In =====")
        
        # Collecting User ID and Password from student
        user_id = input("Enter User ID: ")
        password = input("Enter Password: ")

        print("\n1. Sign-In")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Validate the student's credentials in the database
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT * FROM User WHERE user_id=%s AND password=%s AND role='student'", (user_id, password))
                student = cursor.fetchone()

                if student:
                    print("Login successful. Redirecting to Student Landing Page...")
                    # Redirect to the student landing page (function to be implemented)
                    student_landing_page(student[0])  # Passing student id for further operations
                else:
                    print("Login Incorrect. Please check your credentials and try again.")

            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                cursor.close()
                conn.close()

        elif choice == '2':
            # Discard the input and return to the home page
            print("Going back to the Home page...")
            return

        else:
            print("Invalid choice. Please select 1 or 2.")


def student_landing_page(student_id):
    while True:
        print("\n===== Student Landing Page =====")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT c.textbook_id from course c WHERE c.course_id IN (SELECT DISTINCT e.course_id FROM enrollment e WHERE e.student_id = %s AND e.status='approved')", (student_id,))
        textbook_ids = cursor.fetchall()
        for textbook_id in textbook_ids:
            print(f"E-book {textbook_id[0]}")
            cursor.execute("SELECT chapter_id FROM Chapter WHERE textbook_id=%s", (textbook_id[0],))
            chapter_ids = cursor.fetchall()
            for chapter_id in chapter_ids:
                print(f"Chapter {chapter_id[0]}")
                cursor.execute("SELECT section_id, section_number FROM Section WHERE textbook_id=%s AND chapter_id=%s", (textbook_id[0], chapter_id[0]))
                sections = cursor.fetchall()
                for section in sections:
                    print(f"\tSection {section[1]}")
                    cursor.execute("SELECT content_block_id FROM ContentBlock WHERE section_id=%s", (section[0],))
                    block_ids = cursor.fetchall()
                    for block_id in block_ids:
                        print(f"\t\tBlock {block_id[0]}")

        print("\nMenu:")
        print("1. View a section")
        print("2. View participation activity point")
        print("3. Logout")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            # Redirect to view a section function
            view_section(student_id)  # Function to view sections (to be implemented)
        elif choice == '2':
            # Redirect to view participation activity points function
            view_participation_activity_point(student_id)  # Function to view activity (to be implemented)
        elif choice == '3':
            # Logout and return to the login or home page
            print("Logging out... Returning to the home page.")
            return start_menu()
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

# Placeholder for the View Section function
def view_section(student_id):
    while True:
        print("\n===== View Section =====")
        textbook_id = input("Enter Textbook ID: ")
        chapter_id = input("Enter Chapter ID: ")
        section_num = input("Enter Section Number: ")
        # Check if the Chapter ID and Section ID exist in the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT section_id FROM Section WHERE textbook_id = %s AND chapter_id = %s AND section_number = %s", (textbook_id, chapter_id, section_num))
            (section_id,) = cursor.fetchone()

            if not section_id:
                print("Invalid Chapter ID or Section ID. Please enter valid details.")
                continue  # Return to the input prompt if IDs are invalid

        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            cursor.close()
            conn.close()

        # Proceed with the options menu
        print("\nMenu:")
        print("1. View Block")
        print("2. Go Back")
        choice = input("Choose an option (1-2): ")

        if choice == '1':
            # Proceed to view the block in the section
            view_block(textbook_id, chapter_id, section_id, student_id)
        elif choice == '2':
            print("Going back to the previous page...")
            return  # Goes back to the student landing page
        else:
            print("Invalid choice. Please select 1 or 2.")

def view_block(textbook_id, chapter_id, section_id, student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch block details for the given chapter and section
        cursor.execute("SELECT content_block_id, block_type, content FROM ContentBlock WHERE section_id = %s", (section_id,))
        blocks = cursor.fetchall()

        if not blocks:
            print(f"No blocks found for Section {section_id}")
            return

        for block_id, block_type, content in blocks:
            print(f"\n===== Viewing Block {block_id} =====")
            if block_type == 'text' or block_type == 'picture':
                # If it's content, display the content and proceed
                print(f"Content: {content}")
                print("1. Next")
                print("2. Go Back")
                choice = input("Choose an option (1-2): ")

                if choice == '1':
                    continue  # Go to the next block or finish
                elif choice == '2':
                    print("Going back to the previous page...")
                    return
                else:
                    print("Invalid option. Please try again.")
                    return
            elif block_type == 'activity':
                print("Activity")
                activity_id = content
                cursor.execute("SELECT question_id, question_text, option1, option2, option3, option4, explanation1, explanation2, explanation3, explanation4, correct_option FROM Question WHERE section_id = %s AND content_block_id = %s AND activity_id = %s", (section_id, block_id, activity_id))
                
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
                    (textbook_id, chapter_id, section_id, block_id, activity_id, question_id, student_id)
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
                            # score_id = score[0]
                            cursor.execute(f"UPDATE Score SET score = 3, timestamp = '{current_timestamp}' WHERE textbook_id={textbook_id} AND chapter_id='{chapter_id}' AND section_id={section_id} AND content_block_id='{block_id}' AND activity_id='{activity_id}' AND question_id='{question_id}'")
                        else:
                            course_id = input("Enter Course ID: ")
                            cursor.execute(f"INSERT INTO Score(student_id, course_id, textbook_id, section_id, chapter_id, content_block_id, activity_id, question_id, score, feedback, timestamp) VALUES('{student_id}', '{course_id}', '{textbook_id}', '{section_id}', '{chapter_id}', '{block_id}', '{activity_id}', '{question_id}', 3, '', '{current_timestamp}')")
                        conn.commit()
                    else:
                        print("Incorrect answer. You lost 1 point. Here's the explanation...")
                        explanation = explanations[int(correct_answer) - 1]
                        print(explanation)
                        if score:
                            # score_id = score[0]
                            cursor.execute(f"UPDATE Score SET score = -1, timestamp = '{current_timestamp}' WHERE textbook_id={textbook_id} AND chapter_id='{chapter_id}' AND section_id={section_id} AND content_block_id='{block_id}' AND activity_id='{activity_id}' AND question_id='{question_id}'")
                        else:
                            course_id = input("Enter Course ID: ")
                            cursor.execute(f"INSERT INTO Score(student_id, course_id, textbook_id, section_id, chapter_id, content_block_id, activity_id, question_id, score, feedback, timestamp) VALUES('{student_id}', '{course_id}', '{textbook_id}', '{section_id}', '{chapter_id}', '{block_id}', '{activity_id}', '{question_id}', -1, '', '{current_timestamp}')")
                        conn.commit()
                    continue  # Go to the next block or finish
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
        # Retrieve the participation points for the student
        cursor.execute("SELECT SUM(score) FROM Score WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()

        if result:
            participation_points = result[0]
            print(f"\n===== Current Participation Points =====")
            print(f"Your current total participation activity points: {participation_points}")
        else:
            print("No participation points found for this student.")

        # Display menu for going back
        print("\n1. Go back")
        choice = input("Choose an option (1): ")

        if choice == '1':
            print("Going back to the landing page...")
            return  # Go back to the previous menu
        else:
            print("Invalid option. Returning to the landing page...")
            return

    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")
    finally:
        cursor.close()
        conn.close()




def ta_home(ta_id):
    print("Teaching Assistant Home")
    # TA-specific functions go here
    ta_landing_page(ta_id)


def student_home():
    print("Student Home")
    # Student-specific functions go here

def exit_app():
    print("Goodbye!")
    exit()

if __name__ == '__main__':
    start_menu()
