import csv
import random

first_names = ['John', 'Jane', 'Alex', 'Chris', 'Pat', 'Taylor', 'Jordan', 'Morgan', 'Casey', 'Jamie', 'Martina', 'Lewis', 'Daniel', ' Helen', 'Andrew', 'Nero', 'Eson']
second_names = ['Doe', 'Smith', 'Brown', 'Johnson', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Xue', 'Dong', 'Wang', 'He', 'Yu', 'Takahashi', 'Lin']
genders = ['Male', 'Female', 'Non-binary']

def generate_email(first_name, second_name):
    return f'{first_name.lower()}{second_name.lower()}@example.com'

def generate_phone_number():
    return f'{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}'

with open('test_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['firstName', 'secondName', 'gender', 'email', 'phoneNumber'])
    
    for _ in range(10000):
        first_name = random.choice(first_names)
        second_name = random.choice(second_names)
        gender = random.choice(genders)
        email = generate_email(first_name, second_name)
        phone_number = generate_phone_number()
        writer.writerow([first_name, second_name, gender, email, phone_number])

print("CSV file with 10000 rows has been generated.")
