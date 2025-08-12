import mysql.connector as sql
from tkinter import messagebox
import random

# Connect to the database
mydb = sql.connect(
    host="",
    user="",
    passwd="",
    database=""
)
cursor = mydb.cursor()

# Function to execute queries
def db_query(query, params=None):
    cursor.execute(query, params if params else [])
    result = cursor.fetchall()
    return result

# Function to generate a random 10-digit account number
def generate_account_number():
    return random.randint(1000000000, 9999999999)  # Generates a 10-digit number

# Define SignUp class for registration
class SignUp:
    def __init__(self, username, password, name, age, city, account_number=None):
        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.city = city
        # If no account number is passed, generate one automatically
        self.account_number = account_number or generate_account_number()

    def register_user(self):
        try:
            # Check if the username already exists
            check_user_query = f"SELECT * FROM customers WHERE username = %s"
            result = db_query(check_user_query, (self.username,))

            if result:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                return

            # Ensure the account number is within the valid range for BIGINT
            if not (1000000000 <= self.account_number <= 9999999999):
                messagebox.showerror("Error", "Generated account number is out of range.")
                return

            # Insert the new user into the database
            insert_query = f"""
                INSERT INTO customers (username, password, name, age, city, balance, account_number, status)
                VALUES (%s, %s, %s, %s, %s, 0, %s, 1)
            """
            db_query(insert_query, (self.username, self.password, self.name, self.age, self.city, self.account_number))
            mydb.commit()

            # Show success message
            messagebox.showinfo("Registration Successful", "Your account has been created successfully!")
            print(f"User {self.username} registered successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while registering the user: {str(e)}")
            print(f"Error during user registration: {str(e)}")

# Define SignIn class for login
class SignIn:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate_user(self):
        try:
            # Check if the username exists
            check_user_query = f"SELECT * FROM customers WHERE username = %s"
            result = db_query(check_user_query, (self.username,))

            if not result:
                messagebox.showerror("Error", "Username not found.")
                return False

            # Check if the password is correct
            if result[0][1] != self.password:  # Assuming password is stored in result[0][1]
                messagebox.showerror("Error", "Incorrect password.")
                return False

            return True
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while logging in: {str(e)}")
            print(f"Error during user authentication: {str(e)}")
            return False
