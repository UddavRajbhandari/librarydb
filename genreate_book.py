from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Generate Books
print("-- Insert Books")
for _ in range(200):
    title = fake.sentence(nb_words=3).replace("'", "''")  # Avoid SQL errors
    author = fake.name().replace("'", "''")
    isbn = fake.isbn13()
    year = random.randint(1900, 2023)
    category = random.choice(['Fiction', 'Science', 'History', 'Education', 'Technology'])
    quantity = random.randint(1, 10)
    
    print(f"('{title}', '{author}', '{isbn}', {year}, '{category}', {quantity}),")

# # Generate Members
# print("\n-- Insert Members")
# for _ in range(40):
#     full_name = fake.name().replace("'", "''")
#     email = fake.email()
#     phone = fake.random_number(digits=10)
#     address = fake.address().replace("\n", ", ").replace("'", "''")  # Avoid newline issues
    
#     print(f"('{full_name}', '{email}', '{phone}', '{address}'),")

# # Generate Transactions
# print("\n-- Insert Transactions")
# for _ in range(50):
#     member_id = random.randint(1, 40)  # Assuming member IDs are 1-40
#     book_id = random.randint(1, 200)  # Assuming book IDs are 1-200
#     borrow_date = fake.date_between(start_date='-1y', end_date='today')
#     due_date = borrow_date + timedelta(days=14)
    
#     print(f" ({member_id}, {book_id}, '{borrow_date}', '{due_date}'),")

# # Generate Users
# print("\n-- Insert Users")
# for _ in range(80):
#     username = fake.user_name().replace("'", "''")
#     password_hash = fake.sha256()
#     role = random.choice(['Admin', 'Librarian', 'Member'])
    
#     print(f"('{username}', '{password_hash}', '{role}'),")


from datetime import timedelta
import random
from faker import Faker

fake = Faker()

# Insert Members
print("\n-- Insert Members")
for _ in range(40):
    full_name = fake.name().replace("'", "''")
    email = fake.email()
    phone = fake.random_number(digits=10)
    address = fake.address().replace("\n", ", ").replace("'", "''")  # Avoid newline issues
    membership_date = fake.date_this_decade()  # Generate a random membership date in the last decade

    print(f"('{full_name}', '{email}', '{phone}', '{address}', '{membership_date}'),")

# Insert Transactions
print("\n-- Insert Transactions")
for _ in range(50):
    member_id = random.randint(1, 40)  # Assuming member IDs are 1-40
    book_id = random.randint(1, 200)  # Assuming book IDs are 1-200
    borrow_date = fake.date_between(start_date='-1y', end_date='today')
    due_date = borrow_date + timedelta(days=14)
    
    # Randomly select a status: 'Issued', 'Returned', or 'Overdue'
    status = random.choice(['Issued', 'Returned', 'Overdue'])
    
    # For 'Returned' status, generate a return date that is between the borrow date and due date
    return_date = None
    if status == 'Returned':
        return_date = fake.date_between(start_date=borrow_date, end_date=due_date)
    
    # Print the insert statement with return_date and status
    print(f"({member_id}, {book_id}, '{borrow_date}', '{due_date}', '{return_date if return_date else 'NULL'}', '{status}'),")
