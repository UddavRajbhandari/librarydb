
import pandas as pd
import pyodbc  # Use pyodbc for MSSQL connection
import streamlit as st

# Function to create connection to MSSQL
def create_connection():
    # Replace with your MSSQL server credentials
    server = 'DESKTOP-58K32MS'  # e.g., 'localhost' or 'your_server_ip'
    database = 'LibraryDB'  # Your database name
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        st.error(f"Error connecting to SQL Server: {e}")
        return None

# Login Function
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Users WHERE Username = ? AND PasswordHash = ?"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                st.session_state["user"] = {
                    "UserID": user.UserID,
                    "Username": user.Username,
                    "Role": user.Role
                }
                st.success("Logged in successfully!")
                st.rerun()  # Refresh the app
            else:
                st.error("Invalid username or password.")

# Logout Function
def logout():
    if "user" in st.session_state:
        del st.session_state["user"]
        st.success("Logged out successfully!")
        st.rerun()  # Refresh the app

# Add New Book (Admin and Librarian only)
def add_book():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Add New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        category = st.text_input("Category")
        genre = st.text_input("Genre")
        year = st.number_input("Published Year", min_value=1000, max_value=9999)
        quantity = st.number_input("Quantity", min_value=0)

        if st.button("Add Book"):
            # Check if any field is empty
            if not title or not author or not category or not genre:
                st.error("All fields must be filled.")
            elif quantity <= 0:
                st.error("Quantity must be a positive number.")
            else:
                conn = create_connection()
                if conn:
                    cursor = conn.cursor()

                    # Check if the book already exists
                    cursor.execute("SELECT * FROM Books WHERE Title = ? AND Author = ?", (title, author))
                    existing_book = cursor.fetchone()

                    if existing_book:
                        st.error("This book already exists in the database.")
                    else:
                        query = "INSERT INTO Books (Title, Author, Genre, PublishedYear, Category, Quantity) VALUES (?, ?, ?, ?, ?, ?)"
                        cursor.execute(query, (title, author, genre, year, category, quantity))
                        conn.commit()
                        conn.close()
                        st.success("Book added successfully!")

# View All Books (All roles)
def view_books():
    st.title("View Books")
    conn = create_connection()
    if conn:
        query = "SELECT * FROM Books"
        df = pd.read_sql(query, conn)
        conn.close()
        st.dataframe(df)

# Update Book Details (Admin and Librarian only)
def update_book():
    if st.session_state["user"]["Role"] in ["Admin", "Librarian"]:
        st.title("Update Book Details")
        book_id = st.number_input("Book ID", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=0)

        if st.button("Update Book Quantity"):
            # Ensure the quantity is non-negative
            if new_quantity < 0:
                st.error("Quantity cannot be negative.")
            else:
                conn = create_connection()
                if conn:
                    cursor = conn.cursor()
                    query = "UPDATE Books SET Quantity = ? WHERE BookID = ?"
                    cursor.execute(query, (new_quantity, book_id))
                    conn.commit()
                    conn.close()
                    st.success("Book quantity updated successfully!")

# Delete Book (Admin only)
def delete_book():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("Delete Book")
        book_id = st.number_input("Book ID", min_value=1)

        if st.button("Delete Book"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                query = "DELETE FROM Books WHERE BookID = ?"
                cursor.execute(query, (book_id,))
                conn.commit()
                conn.close()
                st.success("Book deleted successfully!")
    else:
        st.error("You do not have permission to perform this action.")

# Export Data to CSV
def export_to_csv():
    st.title("Export Data to CSV")
    conn = create_connection()
    if conn:
        # Export Books
        if st.button("Export Books"):
            try:
                query = "SELECT * FROM Books"
                df = pd.read_sql(query, conn)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Books CSV",
                    data=csv,
                    file_name="books_data.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error exporting Books: {e}")

        # Export Members
        if st.button("Export Members"):
            try:
                query = "SELECT * FROM Members"
                df = pd.read_sql(query, conn)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Members CSV",
                    data=csv,
                    file_name="members_data.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error exporting Members: {e}")

        # Export Transactions
        if st.button("Export Transactions"):
            try:
                query = "SELECT * FROM Transactions"
                df = pd.read_sql(query, conn)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Transactions CSV",
                    data=csv,
                    file_name="transactions_data.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error exporting Transactions: {e}")

        # Export Users
        if st.button("Export Users"):
            try:
                query = "SELECT * FROM Users"
                df = pd.read_sql(query, conn)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Users CSV",
                    data=csv,
                    file_name="users_data.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Error exporting Users: {e}")

        conn.close()

# Borrow Books (Member only)
def borrow_book():
    if st.session_state["user"]["Role"] == "Member":
        st.title("Borrow a Book")
        member_id = st.session_state["user"]["UserID"]
        book_id = st.number_input("Book ID", min_value=1)
        due_date = st.date_input("Due Date")

        if st.button("Borrow Book"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()

                try:
                    # Check if the book exists
                    cursor.execute("SELECT Quantity FROM Books WHERE BookID = ?", (book_id,))
                    result = cursor.fetchone()

                    if result is None:
                        st.error("Book not found.")
                    else:
                        quantity = result.Quantity

                        if quantity > 0:
                            # Insert transaction
                            query = "INSERT INTO Transactions (MemberID, BookID, DueDate, Status) VALUES (?, ?, ?, 'Issued')"
                            cursor.execute(query, (member_id, book_id, due_date))

                            # Update book quantity
                            cursor.execute("UPDATE Books SET Quantity = Quantity - 1 WHERE BookID = ?", (book_id,))
                            conn.commit()
                            st.success("Book borrowed successfully!")
                        else:
                            st.error("This book is not available.")
                except Exception as e:
                    st.error(f"Error borrowing book: {e}")
                finally:
                    conn.close()
    else:
        st.error("You do not have permission to perform this action.")


# Return Books (Member only)
def return_book():
    user_role = st.session_state["user"]["Role"]
    st.title("Return a Book")
    transaction_id = st.number_input("Transaction ID", min_value=1)

    if st.button("Return Book"):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()

            if user_role == "Member":
                member_id = st.session_state["user"]["UserID"]

                # Check if the transaction belongs to the member
                cursor.execute("SELECT BookID FROM Transactions WHERE TransactionID = ? AND MemberID = ?", 
                               (transaction_id, member_id))
                result = cursor.fetchone()

                if not result:
                    st.error("Invalid Transaction ID or you do not have permission to return this book.")
                    conn.close()
                    return

                book_id = result.BookID

            elif user_role in ["Admin", "Librarian"]:
                # Fetch BookID for the given TransactionID
                cursor.execute("SELECT BookID FROM Transactions WHERE TransactionID = ?", (transaction_id,))
                result = cursor.fetchone()

                if not result:
                    st.error("Invalid Transaction ID.")
                    conn.close()
                    return

                book_id = result.BookID

            else:
                st.error("You do not have permission to perform this action.")
                return

            # Update transaction status
            cursor.execute("UPDATE Transactions SET ReturnDate = GETDATE(), Status = 'Returned' WHERE TransactionID = ?", 
                           (transaction_id,))

            # Update book quantity
            cursor.execute("UPDATE Books SET Quantity = Quantity + 1 WHERE BookID = ?", (book_id,))
            conn.commit()
            conn.close()
            st.success("Book returned successfully!")

# Add New User (Admin only)
def add_user():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Librarian", "Member"])

        if st.button("Add User"):
            # Check if any field is empty
            if not username or not password:
                st.error("Username and Password cannot be empty.")
            else:
                conn = create_connection()
                if conn:
                    cursor = conn.cursor()

                    # Check if the username already exists
                    cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
                    existing_user = cursor.fetchone()

                    if existing_user:
                        st.error("Username already exists. Please choose a different username.")
                    else:
                        query = "INSERT INTO Users (Username, PasswordHash, Role) VALUES (?, ?, ?)"
                        cursor.execute(query, (username, password, role))
                        conn.commit()
                        conn.close()
                        st.success("User added successfully!")


# View All Users (Admin only)
def view_users():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("View Users")
        conn = create_connection()
        if conn:
            query = "SELECT * FROM Users"
            df = pd.read_sql(query, conn)
            conn.close()
            st.dataframe(df)
    else:
        st.error("You do not have permission to perform this action.")
# View All Members (Admin only)
def view_members():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("View Members")
        conn = create_connection()
        if conn:
            query = "SELECT * FROM Members"
            df = pd.read_sql(query, conn)
            conn.close()
            st.dataframe(df)
    else:
        st.error("You do not have permission to perform this action.")

# Add New Member (Admin only)
def add_member():
    if st.session_state["user"]["Role"] == "Admin":
        st.title("Add New Member")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_input("Address")

        if st.button("Add Member"):
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                query = "INSERT INTO Members (FullName, Email, Phone, Address) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (full_name, email, phone, address))
                conn.commit()
                conn.close()
                st.success("Member added successfully!")
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
            if conn:
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
        if conn:
            query = "SELECT * FROM Transactions"
            df = pd.read_sql(query, conn)
            conn.close()
            st.dataframe(df)
    else:
        st.error("You do not have permission to perform this action.")

# Main App Logic
def main():
    st.sidebar.title("Library Management System")

    if "user" not in st.session_state:
        login()
    else:
        with st.sidebar.expander("👤 Profile", expanded=False):
            st.write(f"*Username:* {st.session_state['user']['Username']}")
            st.write(f"*Role:* {st.session_state['user']['Role']}")
            if st.button("Logout", key="logout_button"):
                logout()

        menu_options = {
            "Admin": [
                "Add Book", "View Books", "Update Book", "Delete Book", "Export to CSV",
                "Issue Book", "View Transactions", "Return Book",
                "Add User", "View Users", "Add Member", "View Members"
            ],
            "Librarian": [
                "Add Book", "View Books", "Update Book", "Export to CSV",
                "Issue Book", "View Transactions", "Return Book"
            ],
            "Member": [
                "View Books", "Borrow Book", "Return Book"
            ]
        }

        role = st.session_state["user"]["Role"]
        option = st.sidebar.selectbox(
            "📌 Choose an Operation:", 
            menu_options[role], 
            index=0,  # Sets default selection to the first item
            placeholder="Select an option"  # Ensures no typing
        )

        st.markdown(
            """
            <style>
                /* Remove blinking cursor inside the selectbox */
                div[data-baseweb="select"] input {
                    caret-color: transparent !important;
                }

                /* Change cursor to pointer when hovering over the selectbox */
                div[data-baseweb="select"] > div { 
                    cursor: pointer !important; 
                }
            </style>
            """,
            unsafe_allow_html=True
        )

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
        elif option == "Borrow Book":
            borrow_book()
        elif option == "Add Member":  # New option
            add_member()
        elif option == "View Members":  # New option
            view_members()

# Run the app
if __name__ == "__main__":
    main()