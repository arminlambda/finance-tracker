#small little project of my own, its an overly simple finance tracker with a gui, that helps me track where i spent the money. in the future
#i will add an update where it tracks my money and make it into a mobile phone app



import sqlite3
import tkinter as tk
from tkinter import messagebox

def connect_db():
    return sqlite3.connect('C:\\pprojekt\\finances.db')  # Ensure this path is correct

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY,
            date TEXT,
            description TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_record(date, description, amount):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO finances (date, description, amount) VALUES (?, ?, ?)', (date, description, amount))
        conn.commit()
        conn.close()
        print("Record added successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_records():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM finances')
        records = cursor.fetchall()
        conn.close()
        return records
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []

def update_record(record_id, date, description, amount):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE finances
            SET date = ?, description = ?, amount = ?
            WHERE id = ?
        ''', (date, description, amount, record_id))
        conn.commit()
        conn.close()
        print("Record updated successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_record(record_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM finances WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
        print("Record deleted successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


def add_record_gui():
    date = date_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    if date and description and amount:
        try:
            add_record(date, description, float(amount))
            messagebox.showinfo("Success", "Record added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")

def view_records_gui():
    records = view_records()
    records_window = tk.Toplevel(root)
    records_window.title("Financial Records")
    for record in records:
        record_label = tk.Label(records_window, text=str(record))
        record_label.pack()

create_table()

root = tk.Tk()
root.title("Personal Finance Tracker")

tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Description:").pack()
description_entry = tk.Entry(root)
description_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Record", command=add_record_gui).pack()
tk.Button(root, text="View Records", command=view_records_gui).pack()


root.mainloop()
