import tkinter as tk
from tkinter import messagebox
from register import SignIn, SignUp  # Import SignIn and SignUp classes/functions
from bank import Bank
from database import db_query
from PIL import Image, ImageTk
import threading
import random

# Global variables for user
current_user = None

# Function to handle database operations in a separate thread
def handle_database_operations(action, username=None, password=None, name=None, age=None, city=None, account_number=None):
    global current_user  # Use the global variable to store current_user
    
    if action == 'sign_up':
        # Create an instance of SignUp with the user data
        sign_up_obj = SignUp(username, password, name, age, city, account_number)
        sign_up_obj.register_user()  # Register user in the database
    elif action == 'sign_in' and username and password:
        current_user = SignIn(username, password)  # Create SignIn instance with username and password
        if current_user.authenticate_user():  # Authenticate user
            show_main_menu(current_user.username)  # If successful, show the main menu
        else:
            messagebox.showerror("Error", "Invalid credentials!")  # Show error message for invalid credentials

# Set up the main Tkinter window
root = tk.Tk()
root.title("Mafia Banking System")
root.geometry("400x500")

# Add background image
bg_image = Image.open(r"C:\Users\hp\Desktop\The-Future-of-Finance-Embracing-Open-Banking-980x653.png").resize((400, 500))
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create main screen UI
def create_main_screen():
    label = tk.Label(root, text="Welcome to Mafia Banking", font=("Arial", 24, "bold"), bg="#E0F7FA")
    label.pack(pady=30)

    sign_up_button = tk.Button(root, text="Sign Up", command=sign_up, width=20, height=2, bg="#4CAF50", fg="white")
    sign_up_button.pack(pady=10)

    sign_in_button = tk.Button(root, text="Sign In", command=sign_in, width=20, height=2, bg="#008CBA", fg="white")
    sign_in_button.pack(pady=10)

    # Add footer
    footer_label = tk.Label(root, text="Mafia Bank Ltd. © 2025", font=("Arial", 10), bg="#E0F7FA")
    footer_label.pack(side=tk.BOTTOM, pady=10)

# Handle SignUp action
def sign_up():
    def generate_account_number():
        return random.randint(1000000000, 9999999999)

    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        name = entry_name.get()
        age = entry_age.get()
        city = entry_city.get()

        # Generate account number here
        account_number = generate_account_number()

        # Start database operations in a thread
        threading.Thread(target=handle_database_operations, args=('sign_up', username, password, name, age, city, account_number)).start()

        sign_up_window.destroy()

    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("300x300")

    tk.Label(sign_up_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(sign_up_window)
    entry_username.pack(pady=5)

    tk.Label(sign_up_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(sign_up_window, show="*")
    entry_password.pack(pady=5)

    tk.Label(sign_up_window, text="Name:").pack(pady=5)
    entry_name = tk.Entry(sign_up_window)
    entry_name.pack(pady=5)

    tk.Label(sign_up_window, text="Age:").pack(pady=5)
    entry_age = tk.Entry(sign_up_window)
    entry_age.pack(pady=5)

    tk.Label(sign_up_window, text="City:").pack(pady=5)
    entry_city = tk.Entry(sign_up_window)
    entry_city.pack(pady=5)

    sign_up_button = tk.Button(sign_up_window, text="Register", command=register_user, bg="#4CAF50", fg="white")
    sign_up_button.pack(pady=10)

# Handle SignIn action
def sign_in():
    def sign_in_user():
        username = entry_username.get()
        password = entry_password.get()
        threading.Thread(target=handle_database_operations, args=('sign_in', username, password)).start()

    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")
    sign_in_window.geometry("300x200")

    tk.Label(sign_in_window, text="Username:").pack(pady=10)
    entry_username = tk.Entry(sign_in_window)
    entry_username.pack(pady=5)

    tk.Label(sign_in_window, text="Password:").pack(pady=10)
    entry_password = tk.Entry(sign_in_window, show="*")
    entry_password.pack(pady=5)

    sign_in_button = tk.Button(sign_in_window, text="Sign In", command=sign_in_user, bg="#008CBA", fg="white")
    sign_in_button.pack(pady=10)

# Show the main menu after successful login
def show_main_menu(username):
    for widget in root.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(root, text=f"Welcome {username.capitalize()}!", font=("Arial", 18), bg="#E0F7FA")
    welcome_label.pack(pady=20)

    def banking_service(service):
        account_number = get_account_number(username)
        if not account_number:
            messagebox.showerror("Error", "Account number not found.")
            return

        bobj = Bank(username, account_number)
        if service == 1:
            bobj.balance_enquiry()
        elif service == 2:
            deposit_amount_ui(bobj)
        elif service == 3:
            withdraw_amount_ui(bobj)
        elif service == 4:
            transfer_funds_ui(bobj)

    def deposit_amount_ui(bobj):
        def perform_deposit():
            try:
                amount = float(entry_amount.get())
                bobj.deposit(amount)
                deposit_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")

        deposit_window = tk.Toplevel(root)
        deposit_window.title("Deposit")
        deposit_window.geometry("300x150")

        tk.Label(deposit_window, text="Enter Deposit Amount:").pack(pady=10)
        entry_amount = tk.Entry(deposit_window)
        entry_amount.pack(pady=5)

        deposit_button = tk.Button(deposit_window, text="Deposit", command=perform_deposit, bg="#4CAF50", fg="white")
        deposit_button.pack(pady=10)

    def withdraw_amount_ui(bobj):
        def perform_withdraw():
            try:
                amount = float(entry_amount.get())
                bobj.withdraw(amount)
                withdraw_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")

        withdraw_window = tk.Toplevel(root)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("300x150")

        tk.Label(withdraw_window, text="Enter Withdrawal Amount:").pack(pady=10)
        entry_amount = tk.Entry(withdraw_window)
        entry_amount.pack(pady=5)

        withdraw_button = tk.Button(withdraw_window, text="Withdraw", command=perform_withdraw, bg="#FF5733", fg="white")
        withdraw_button.pack(pady=10)

    def transfer_funds_ui(bobj):
        def perform_transfer():
            try:
                receiver_account = entry_receiver_account.get()
                amount = float(entry_transfer_amount.get())
                bobj.fund_transfer(receiver_account, amount)
                transfer_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid inputs.")

        transfer_window = tk.Toplevel(root)
        transfer_window.title("Fund Transfer")
        transfer_window.geometry("300x200")

        tk.Label(transfer_window, text="Receiver Account:").pack(pady=10)
        entry_receiver_account = tk.Entry(transfer_window)
        entry_receiver_account.pack(pady=5)

        tk.Label(transfer_window, text="Transfer Amount:").pack(pady=10)
        entry_transfer_amount = tk.Entry(transfer_window)
        entry_transfer_amount.pack(pady=5)

        transfer_button = tk.Button(transfer_window, text="Transfer", command=perform_transfer, bg="#FF5733", fg="white")
        transfer_button.pack(pady=10)

    def get_account_number(username):
        query = f"SELECT account_number FROM customers WHERE username = '{username}';"
        result = db_query(query)
        return result[0][0] if result else None

    options = [
        ("Balance Enquiry", 1),
        ("Deposit", 2),
        ("Withdraw", 3),
        ("Fund Transfer", 4),
    ]

    for text, value in options:
        tk.Button(root, text=text, command=lambda s=value: banking_service(s), width=20, height=2, bg="#4CAF50", fg="white").pack(pady=5)

    tk.Button(root, text="Exit", command=root.quit, width=20, height=2, bg="#FF5733", fg="white").pack(pady=10)

# Start the application
create_main_screen()

# Run the Tkinter event loop
root.mainloop()
