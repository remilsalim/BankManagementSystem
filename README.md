# Bank Management System 🏦

A **Tkinter-based desktop banking system** with **MySQL backend**.  
Supports account creation, login authentication, and banking operations such as **balance enquiry**, **deposit**, **withdrawal**, and **fund transfers**.

---

## 📌 Features

- User Registration (Sign Up) with unique account number generation.
- Secure Login (Sign In) with password validation.
- Balance enquiry.
- Deposit money.
- Withdraw money (with insufficient funds check).
- Transfer funds to other accounts.
- Transaction logging in a universal transaction table.
- Multi-threaded operations for a responsive UI.
- Modern Tkinter UI with a background image.

---

## 🛠 Requirements

- **Python 3.x**
- **MySQL Server**
- Python libraries:
  ```bash
  pip install mysql-connector-python pillow
  ```

---

## ⚙️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/remilsalim/BankManagementSystem.git
   cd BankManagementSystem
   ```

2. **Set up the MySQL database**

   ```sql
   CREATE DATABASE bank;
   USE bank;

   CREATE TABLE customers (
       username VARCHAR(20) NOT NULL,
       password VARCHAR(20) NOT NULL,
       name VARCHAR(20) NOT NULL,
       age INT NOT NULL,
       city VARCHAR(20) NOT NULL,
       balance INT NOT NULL,
       account_number BIGINT NOT NULL,
       status BOOLEAN NOT NULL
   );

   CREATE TABLE qwerty_transaction (
       timedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       account_number BIGINT NOT NULL,
       transaction_type VARCHAR(50) NOT NULL,
       amount DECIMAL(10,2) NOT NULL,
       status VARCHAR(20) NOT NULL
   );
   ```

3. **Update database credentials**

   - In `database.py` and `register.py`, set your MySQL:
     ```python
     host="localhost",
     user="root",
     passwd="yourpassword",
     database="bank"
     ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 👤 Author

**Remil Salim**  
[GitHub Profile](https://github.com/remilsalim)
