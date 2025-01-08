import csv
import random

# Function to generate random email providers
def random_email_provider():
    providers = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "icloud.com"]
    return random.choice(providers)

# Function to generate random phone numbers with international country code
def random_phone_number():
    country_codes = ["+1", "+44", "+61", "+81", "+33", "+49", "+91", "+34"]
    return f"{random.choice(country_codes)}-{random.randint(1000000000, 9999999999)}"

# Sample data for first names and second names
first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Daisy", "Eve", "Frank", "Martina", "Lewis", "Nero", "Eson", "Helen", "Saito", "Helion", "Tenji"]
second_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Wilson", "Moore", "Dong", "Xue", "Takahashi", "Lin", "He", "Renji", "Marksman","Togifushi"]

# Field names
fields = ["firstName", "secondName", "email", "gender", "phoneNumber"]

# Generating 100 records
records = []
for _ in range(100000):
    first_name = random.choice(first_names)
    second_name = random.choice(second_names)
    email = f"{first_name.lower()}.{second_name.lower()}@{random_email_provider()}"
    gender = random.choice(["Male", "Female", "Non-Binary"])
    phone_number = random_phone_number()
    records.append([first_name, second_name, email, gender, phone_number])

# Writing to CSV file
with open("data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(records)

print("CSV file created successfully.")
