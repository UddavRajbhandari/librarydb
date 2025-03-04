# app.py
import streamlit as st
import sqlite3
import pandas as pd

# Function to create connection to SQLite
def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

# Create Operation: Add New Book
def add_book():
    st.title("Add New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    publisher = st.text_input("Publisher")
    genre = st.text_input("Genre")
    year = st.number_input("Published Year", min_value=1000, max_value=9999)
    quantity = st.number_input("Quantity", min_value=1)

    if st.button("Add Book"):
        conn = create_connection()
        cursor = conn.cursor()
        query = "INSERT INTO Books (Title, Author, Publisher, Genre, PublishedYear, Quantity) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (title, author, publisher, genre, year, quantity))
        conn.commit()
        conn.close()
        st.success("Book added successfully!")

# Read Operation: View All Books
def view_books():
    st.title("View Books")
    conn = create_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Books"
    cursor.execute(query)
    books = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(books, columns=["BookID", "Title", "Author", "Publisher", "Genre", "PublishedYear", "Quantity"])
    st.dataframe(df)

# Update Operation: Update Book Details (Quantity)
def update_book():
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

# Delete Operation: Remove Book
def delete_book():
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

# Export to CSV (Backup Data)
def export_to_csv():
    st.title("Export Books to CSV")
    conn = create_connection()
    query = "SELECT * FROM Books"
    df = pd.read_sql(query, conn)
    df.to_csv('D:\dbms\librarydb\data\books_data.csv', index=False)
    conn.close()
    st.success("Data exported to books_data.csv")

# Streamlit Sidebar for Navigation
st.sidebar.title("Library Management System")
option = st.sidebar.selectbox("Choose Operation", ("Add Book", "View Books", "Update Book", "Delete Book", "Export to CSV"))

# Execute corresponding function based on user selection
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
