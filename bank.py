import tkinter as tk
from tkinter import messagebox
from database import db_query, mydb
import datetime
import threading

class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

    # Balance Enquiry Method
    def balance_enquiry(self):
        threading.Thread(target=self._perform_balance_enquiry).start()

    def _perform_balance_enquiry(self):
        try:
            # Fetch current balance
            query = f"SELECT balance FROM customers WHERE username = '{self.__username}';"
            temp = db_query(query)
            current_balance = temp[0][0] if temp else 0

            # Display the balance
            messagebox.showinfo("Balance Enquiry", f"Your current balance is: {current_balance}")
            print(f"{self.__username} Balance: {current_balance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during balance enquiry: {str(e)}")
            print(f"Error during balance enquiry: {str(e)}")

    # Deposit Method
    def deposit(self, amount):
        threading.Thread(target=self._perform_deposit, args=(amount,)).start()

    def _perform_deposit(self, amount):
        try:
            # Fetch current balance
            query = f"SELECT balance FROM customers WHERE username = '{self.__username}';"
            temp = db_query(query)
            current_balance = temp[0][0] if temp else 0

            # Update the balance
            updated_balance = current_balance + amount
            update_query = f"UPDATE customers SET balance = '{updated_balance}' WHERE username = '{self.__username}';"
            db_query(update_query)

            # Log the transaction in the universal transaction table
            transaction_query = f"""
                INSERT INTO qwerty_transaction 
                (timedate, account_number, transaction_type, amount, status) 
                VALUES 
                (CURRENT_TIMESTAMP, '{self.__account_number}', 'Deposit', {amount}, 'Success')
            """
            db_query(transaction_query)
            mydb.commit()

            # Display confirmation message
            messagebox.showinfo("Deposit Successful", f"Successfully deposited {amount} into your account.\nNew Balance: {updated_balance}")
            print(f"{self.__username} Balance after deposit: {updated_balance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during deposit: {str(e)}")
            print(f"Error during deposit: {str(e)}")

    # Withdraw Method
    def withdraw(self, amount):
        threading.Thread(target=self._perform_withdraw, args=(amount,)).start()

    def _perform_withdraw(self, amount):
        try:
            # Fetch current balance
            query = f"SELECT balance FROM customers WHERE username = '{self.__username}';"
            temp = db_query(query)
            current_balance = temp[0][0] if temp else 0

            # Check for sufficient balance
            if amount > current_balance:
                messagebox.showwarning("Insufficient Funds", "You do not have enough balance to perform this withdrawal.")
                print(f"{self.__username} attempted to withdraw {amount} but has insufficient funds.")
                return

            # Update the balance
            updated_balance = current_balance - amount
            update_query = f"UPDATE customers SET balance = '{updated_balance}' WHERE username = '{self.__username}';"
            db_query(update_query)

            # Log the transaction in the universal transaction table
            transaction_query = f"""
                INSERT INTO qwerty_transaction 
                (timedate, account_number, transaction_type, amount, status) 
                VALUES 
                (CURRENT_TIMESTAMP, '{self.__account_number}', 'Withdraw', {amount}, 'Success')
            """
            db_query(transaction_query)
            mydb.commit()

            # Display confirmation message
            messagebox.showinfo("Withdrawal Successful", f"Successfully withdrew {amount} from your account.\nNew Balance: {updated_balance}")
            print(f"{self.__username} Balance after withdrawal: {updated_balance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during withdrawal: {str(e)}")
            print(f"Error during withdrawal: {str(e)}")

    # Fund Transfer Method
    def fund_transfer(self, receive_account_number, amount):
        threading.Thread(target=self._perform_fund_transfer, args=(receive_account_number, amount)).start()

    def _perform_fund_transfer(self, receive_account_number, amount):
        try:
            # Fetch sender's current balance
            query_sender = f"SELECT balance FROM customers WHERE username = '{self.__username}';"
            temp_sender = db_query(query_sender)
            sender_balance = temp_sender[0][0] if temp_sender else 0

            # Check for sufficient balance
            if amount > sender_balance:
                messagebox.showwarning("Insufficient Funds", "You do not have enough balance to perform this fund transfer.")
                print(f"{self.__username} attempted to transfer {amount} but has insufficient funds.")
                return

            # Fetch receiver's username
            query_receiver_username = f"SELECT username FROM customers WHERE account_number = '{receive_account_number}';"
            temp_receiver_username = db_query(query_receiver_username)
            if not temp_receiver_username:
                messagebox.showerror("Invalid Account", "The receiver's account number does not exist.")
                print(f"{self.__username} attempted to transfer to invalid account number: {receive_account_number}")
                return
            receiver_username = temp_receiver_username[0][0]

            # Fetch receiver's current balance
            query_receiver_balance = f"SELECT balance FROM customers WHERE account_number = '{receive_account_number}';"
            temp_receiver_balance = db_query(query_receiver_balance)
            receiver_balance = temp_receiver_balance[0][0] if temp_receiver_balance else 0

            # Update sender's balance
            updated_sender_balance = sender_balance - amount
            update_sender_query = f"UPDATE customers SET balance = '{updated_sender_balance}' WHERE username = '{self.__username}';"
            db_query(update_sender_query)

            # Update receiver's balance
            updated_receiver_balance = receiver_balance + amount
            update_receiver_query = f"UPDATE customers SET balance = '{updated_receiver_balance}' WHERE account_number = '{receive_account_number}';"
            db_query(update_receiver_query)

            # Log the transactions in the universal transaction table
            transaction_sender = f"""
                INSERT INTO qwerty_transaction 
                (timedate, account_number, transaction_type, amount, status) 
                VALUES 
                (CURRENT_TIMESTAMP, '{self.__account_number}', 'Fund Transfer to {receive_account_number}', {amount}, 'Success')
            """
            db_query(transaction_sender)

            transaction_receiver = f"""
                INSERT INTO qwerty_transaction 
                (timedate, account_number, transaction_type, amount, status) 
                VALUES 
                (CURRENT_TIMESTAMP, '{receive_account_number}', 'Fund Transfer from {self.__account_number}', {amount}, 'Success')
            """
            db_query(transaction_receiver)
            mydb.commit()

            # Display confirmation message
            messagebox.showinfo("Fund Transfer Successful", f"Successfully transferred {amount} to account {receive_account_number}.\nYour New Balance: {updated_sender_balance}")
            print(f"{self.__username} Balance after fund transfer: {updated_sender_balance}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during fund transfer: {str(e)}")
            print(f"Error during fund transfer: {str(e)}")
