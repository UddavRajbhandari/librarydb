# Library Management System

This project is a **Library Management System** built using Python, Streamlit, and either SQLite or Microsoft SQL Server (MSSQL) as the database backend. It provides a user-friendly interface for managing books, members, transactions, and users in a library.

---

## Features

### **User Roles**
The application supports three user roles, each with specific permissions:

1. **Admin**:
   - Full access to manage books, users, and transactions.
   - Can add, update, delete, and view books.
   - Can add new users and view all users.
   - Can export data (books, members, transactions, users) to CSV.
   - Can issue and return books on behalf of members.

2. **Librarian**:
   - Can manage books and transactions.
   - Can add, update, and view books.
   - Can issue and return books.
   - Can view all transactions.
   - Can export data to CSV.

3. **Member**:
   - Can view the list of available books.
   - Can borrow and return books.

---

### **Functionalities**
- **Books Management**:
  - Add new books with details like title, author, genre, published year, category, and quantity.
  - Update book details (e.g., quantity).
  - Delete books.
  - View all books in a tabular format.

- **Transactions Management**:
  - Issue books to members.
  - Return books and update the status.
  - View all transactions (issued, returned, overdue).

- **Members Management**:
  - Add new members with details like name, email, phone, and address.
  - View all members.

- **Users Management**:
  - Add new users with roles (Admin, Librarian, Member).
  - View all users.

- **Data Export**:
  - Export data (books, members, transactions, users) to CSV files.

---

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Python 3.8+**
2. **Required Python Libraries**:
   Install the required libraries using the following command:
   ```bash
   pip install streamlit pandas pyodbc
   ```

---

## Database Setup

### **For SQLite**
- No additional setup is required.
- The database is automatically created when you run the app.

### **For MSSQL**
1. Install MSSQL Server and create a database named `LibraryDB`.
2. Use the provided SQL script (`library_db.sql`) to create tables and insert sample data.

---

## Project Structure
```
library-management-system/
├── app.py               # Streamlit app for SQLite version
├── sql_app.py           # Streamlit app for MSSQL version
├── library_db.sql       # SQL script for MSSQL database setup
├── README.md            # Project documentation
└── requirements.txt     # List of Python dependencies
```

---

## Setup and Running the Application

### **1. SQLite Version (`app.py`)**
#### Steps:
- Clone the repository:
  ```bash
  git clone https://github.com/your-username/library-management-system.git
  ```
- Navigate to the project directory:
  ```bash
  cd library-management-system
  ```
- Run the SQLite app:
  ```bash
  streamlit run app.py
  ```

**Database:**
- The SQLite database (`library.db`) is automatically created when you run the app.
- No additional setup is required.

---

### **2. MSSQL Version (`sql_app.py`)**
#### Steps:
1. Set up the MSSQL database:
   - Run the provided SQL script (`library_db.sql`) to create the `LibraryDB` database and populate it with sample data.
   - The script creates the following tables:
     - `Books`
     - `Members`
     - `Transactions`
     - `Users`
   - It also inserts sample data for testing.

2. Update the connection details in `sql_app.py`:
   ```python
   server = 'DESKTOP-58K32MS'  # Replace with your MSSQL server name
   database = 'LibraryDB'      # Replace with your database name
   ```

3. Run the MSSQL app:
   ```bash
   streamlit run sql_app.py
   ```

---

## Usage

### **1. Login**
- Open the application in your browser.
- Use the following sample credentials to log in:
  - **Admin:** `admin1` / `adminpass`
  - **Librarian:** `librarian1` / `librarianpass`
  - **Member:** `member1` / `memberpass`

### **2. Navigate the App**
- Use the sidebar to select operations based on your role.
- **Admin:**
  - Add, update, delete, and view books.
  - Add new users and view all users.
  - Export data to CSV.
  - Issue and return books.
- **Librarian:**
  - Add, update, and view books.
  - Issue and return books.
  - View all transactions.
  - Export data to CSV.
- **Member:**
  - View books.
  - Borrow and return books.

---



---

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to the branch.
4. Submit a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
- Built with using Streamlit.
- Database support for SQLite and MSSQL.



