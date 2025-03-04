import os
import io
import pandas as pd
import sqlite3
import streamlit as st

# Function to create connection to SQLite
def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

# Login Function
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Users WHERE Username = ? AND PasswordHash = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state["user"] = {
                "UserID": user[0],
                "Username": user[1],
                "Role": user[3]
            }
            st.success("Logged in successfully!")
            # Force a refresh by updating a dummy session state variable
            st.session_state["refresh"] = not st.session_state.get("refresh", False)
        else:
            st.error("Invalid username or password.")

# Logout Function
def logout():
    if "user" in st.session_state:
        del st.session_state["user"]
        st.success("Logged out successfully!")
        # Force a refresh by updating a dummy session state variable
        st.session_state["refresh"] = not st.session_state.get("refresh", False)

# Add New Book (Admin and Librarian only)
def add_book():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Add New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        category = st.text_input("Category")
        genre = st.text_input("Genre")
        year = st.number_input("Published Year", min_value=1000, max_value=9999)
        quantity = st.number_input("Quantity", min_value=1)

        if st.button("Add Book"):
            conn = create_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Books (Title, Author, Genre, PublishedYear, Category, Quantity) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (title, author, genre, year, category, quantity))
            conn.commit()
            conn.close()
            st.success("Book added successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# View All Books (All roles)
def view_books():
    st.title("View Books")
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Books"
    cursor.execute(query)
    books = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(books, columns=["BookID", "Title", "Author", "Genre", "PublishedYear", "Category", "Quantity"])
    st.dataframe(df)

# Update Book Details (Admin and Librarian only)
def update_book():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Update Book Details")
        book_id = st.number_input("Book ID", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=0)

        if st.button("Update Book Quantity"):
            conn = create_connection()
            cursor = conn.cursor()
            query = "UPDATE Books SET Quantity = ? WHERE BookID = ?"
            cursor.execute(query, (new_quantity, book_id))
            conn.commit()
            conn.close()
            st.success("Book quantity updated successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# Delete Book (Admin only)
def delete_book():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("Delete Book")
        book_id = st.number_input("Book ID", min_value=1)

        if st.button("Delete Book"):
            conn = create_connection()
            cursor = conn.cursor()
            query = "DELETE FROM Books WHERE BookID = ?"
            cursor.execute(query, (book_id,))
            conn.commit()
            conn.close()
            st.success("Book deleted successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# Export Books Data to CSV (Admin and Librarian only)
def export_to_csv():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Export Books to CSV")
        conn = create_connection()
        query = "SELECT * FROM Books"
        df = pd.read_sql(query, conn)
        conn.close()

        save_folder = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        save_path = os.path.join(save_folder, 'books_data.csv')
        df.to_csv(save_path, index=False)
        st.success(f"Data exported successfully to {save_path}")

        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        csv_data = buffer.getvalue().encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="books_data.csv",
            mime="text/csv"
        )
    else:
        st.error("You do not have permission to perform this action.")

# Issue a Book (Admin and Librarian only)
def issue_book():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Issue a Book")
        member_id = st.number_input("Member ID", min_value=1)
        book_id = st.number_input("Book ID", min_value=1)
        due_date = st.date_input("Due Date")

        if st.button("Issue Book"):
            conn = create_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Transactions (MemberID, BookID, DueDate, Status) VALUES (?, ?, ?, 'Issued')"
            cursor.execute(query, (member_id, book_id, due_date))
            conn.commit()
            conn.close()
            st.success("Book issued successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# View All Transactions (Admin and Librarian only)
def view_transactions():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("View Transactions")
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Transactions"
        cursor.execute(query)
        transactions = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(transactions, columns=["TransactionID", "MemberID", "BookID", "IssueDate", "DueDate", "ReturnDate", "Status"])
        st.dataframe(df)
    else:
        st.error("You do not have permission to perform this action.")

# Return a Book (Admin and Librarian only)
def return_book():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Return a Book")
        transaction_id = st.number_input("Transaction ID", min_value=1)

        if st.button("Return Book"):
            conn = create_connection()
            cursor = conn.cursor()
            query = "UPDATE Transactions SET ReturnDate = DATE('now'), Status = 'Returned' WHERE TransactionID = ?"
            cursor.execute(query, (transaction_id,))
            conn.commit()
            conn.close()
            st.success("Book returned successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# Add New User (Admin only)
def add_user():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Librarian", "Member"])

        if st.button("Add User"):
            conn = create_connection()
            cursor = conn.cursor()
            query = "INSERT INTO Users (Username, PasswordHash, Role) VALUES (?, ?, ?)"
            cursor.execute(query, (username, password, role))
            conn.commit()
            conn.close()
            st.success("User added successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# View All Users (Admin only)
def view_users():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("View Users")
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Users"
        cursor.execute(query)
        users = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(users, columns=["UserID", "Username", "PasswordHash", "Role"])
        st.dataframe(df)
    else:
        st.error("You do not have permission to perform this action.")

# Main App Logic
def main():
    st.sidebar.title("Library Management System")

    if "user" not in st.session_state:
        login()
    else:
        st.sidebar.write(f"Logged in as: {st.session_state['user']['Username']} ({st.session_state['user']['Role']})")
        if st.sidebar.button("Logout"):
            logout()

        if "user" in st.session_state:  # Check if user is still logged in
            if st.session_state["user"]["Role"] == "Admin":
                option = st.sidebar.selectbox("Choose Operation", (
                    "Add Book", "View Books", "Update Book", "Delete Book", "Export to CSV",
                    "Issue Book", "View Transactions", "Return Book",
                    "Add User", "View Users"
                ))
            elif st.session_state["user"]["Role"] == "Librarian":
                option = st.sidebar.selectbox("Choose Operation", (
                    "Add Book", "View Books", "Update Book", "Export to CSV",
                    "Issue Book", "View Transactions", "Return Book"
                ))
            elif st.session_state["user"]["Role"] == "Member":
                option = st.sidebar.selectbox("Choose Operation", (
                    "View Books"
                ))

            if option == "Add Book":
                add_book()
            elif option == "View Books":
                view_books()
            elif option == "Update Book":
                update_book()
            elif option == "Delete Book":
                delete_book()
            elif option == "Export to CSV":
                export_to_csv()
            elif option == "Issue Book":
                issue_book()
            elif option == "View Transactions":
                view_transactions()
            elif option == "Return Book":
                return_book()
            elif option == "Add User":
                add_user()
            elif option == "View Users":
                view_users()

# Run the app
if __name__ == "__main__":
    main()