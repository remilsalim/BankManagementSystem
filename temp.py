import random
import time

def generate_account_number():
    for _ in range(5):  # Generate numbers 5 times for animation effect
        random_account_number = random.randint(10000000, 99999999)
        print(f"Generated Account Number: {random_account_number}", end="\r")  # Overwrite previous number
        time.sleep(0.5)

generate_account_number()
