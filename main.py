import sqlite3
import requests
import re
from tabulate import tabulate

# Database connection using sqlite
try:
    my_connection = sqlite3.connect('students.db')
    cur = my_connection.cursor()

    # Creating student table if it doesnot exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INT NOT NULL,
            level TEXT NOT NULL,
            faculty TEXT NOT NULL,
            gender TEXT NOT NULL,
            birthdate DATE NOT NULL,
            email TEXT NOT NULL,
            phone INTEGER NOT NULL,
            address TEXT NOT NULL,
            guardian_name TEXT NOT NULL
        )
    ''')

    # Validating input in fields of name, age, gender, date of birth, email and contact number
    def validate_name():
        while True:
            try:
                input_name = input("Please enter the name of the student: ")
                if 0 < len(input_name) <= 60:
                    return input_name
                else:
                    print("Please enter the name in the range of 1 to 60 characters.")
            except ValueError:
                print("Please enter a valid name.")

    def validate_age():
        while True:
            try:
                input_age = int(input("Enter the age: "))
                if 0 < input_age < 100:
                    return input_age
                else:
                    print("Please enter a valid age. We assume valid age from 0 to 100.")
            except ValueError:
                print("Please enter a valid integer for age.")


    def validate_gender():
        while True:
            try:
                valid_genders = ["Male", "Female", "Others"]
                input_gender = input("Enter the gender: Male, Female or Others: ")
                if input_gender in valid_genders:
                    return input_gender
                else:
                    print("Invalid information. ")
            except ValueError:
                print("Please enter the valid gender. ")


    def validate_date_of_birth():
        while True:
            try:
                input_date = input("Enter the date of birth (YYYY-MM-DD): ")
                if re.match(r"\d{4}-\d{2}-\d{2}$", input_date):
                    return input_date
                else:
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            except ValueError:
                print("Invalid date format")



    def validate_email():
        while True:
            try:
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                input_email = input("Enter the email address: ")
                if re.match(regex, input_email):
                    return input_email
                else:
                    print("Invalid email address.")
            except ValueError:
                print("Please enter a valid email address")

    def validate_phone():
        while True:
            try:
                contact_number = input("Please enter the contact number: ")
                if len(contact_number)<=15:
                    return contact_number
                else:
                    print("Invalid Contact.")
            except ValueError:
                print("Enter valid contact. ")




    # CRUD Operations on Student Information System
    def create():
        name = validate_name()
        age = validate_age()
        level = input("Enter the Academic level of the student: ")
        faculty = input("Enter the respective faculty: ")
        gender = validate_gender()
        birthdate = validate_date_of_birth()
        email = validate_email()
        phone = validate_phone()
        address = input("Enter the contact address:")
        guardian_name = input("Enter the guardian_name:")
        try:
            cur.execute(
                'INSERT INTO students (name, age, level, faculty, gender, birthdate, email, phone, address, guardian_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (name, age, level, faculty, gender, birthdate, email, phone, address, guardian_name))
            my_connection.commit()
            print("You have successfully created a student record.")
        except sqlite3.Error as e:
            print(f"Error occurred while inserting the student record: {e}")


    def retrieve():
        try:
            cur.execute('SELECT * FROM students')
            students = cur.fetchall()
            if students:
                headers = ["ID", "Name", "Age", "Level", "Faculty", "Gender", "Birth Date", "Email", "Phone", "Address",
                           "Guardian Name"]
                rows = []
                for student in students:
                    rows.append(list(student))
                print(tabulate(rows, headers, tablefmt="grid"))
            else:
                print("No students found. Please try again.")
        except sqlite3.Error as e:
            print(f"Error occurred while retrieving student records: {e}")


    def update():
        id = int(input("Enter the student ID to update: "))
        name = validate_name()
        age = validate_age()
        level = input("Enter the modified level: ")
        faculty = input("Enter the modified faculty: ")
        gender = validate_gender()
        birthdate = validate_date_of_birth()
        email = validate_email()
        phone = validate_phone()
        address = input("Enter the modified contact address:")
        guardian_name = input("Enter the guardian_name:")

        try:
            cur.execute(
                'UPDATE students SET name=?, age=?, level=?, faculty=?,gender=?, birthdate=?, email=?, phone=?, address=?, guardian_name=? WHERE id=?',
                (name, age, level, faculty, gender, birthdate, email, phone, address, guardian_name, id))
            my_connection.commit()
            print("You have successfully modified the student record.")
        except sqlite3.Error as e:
            print(f"Error occurred while updating the student record: {e}")


    def delete():
        id = int(input("Enter the student ID to delete: "))
        try:
            cur.execute('DELETE FROM students WHERE id=?', (id,))
            my_connection.commit()
            print("You have successfully deleted the student record.")
        except sqlite3.Error as e:
            print(f"Error occurred while deleting the student record: {e}")


    # While displaying to the user::
    while True:
        print("Welcome to the Students Management System!")
        print("1.\tInsert a student record:")
        print("2.\tRead student record if it exists in the table:")
        print("3.\tUpdate the existing student record:")
        print("4.\tDelete the student record")
        print("0.\tExit")

        choice = input("Enter your choice: ")

        match choice:
            case '1':
                create()
            case '2':
                retrieve()
            case '3':
                update()
            case '4':
                delete()
            case '0':
                print("Goodbyes are harder!!")
                break
            case _:
                print("Invalid choice. Please enter a valid option.")

except sqlite3.Error as e:
    print(f"Error occurred while connecting to the database: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:

    if my_connection:
        my_connection.close()
