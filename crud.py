import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- Database Connection ----------------
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="abc"
)

cursor = conn.cursor()

selected_id = None

# ---------------- Register ----------------
def register():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if name == "" or email == "" or password == "":
        messagebox.showerror("Error", "All Fields Are Required")
        return

    sql = "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
    values = (name, email, password)

    cursor.execute(sql, values)
    conn.commit()

    messagebox.showinfo("Success", "Registration Successful")

    clear()
    show_data()


# ---------------- Show Data ----------------
def show_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)


# ---------------- Clear ----------------
def clear():
    global selected_id

    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_password.delete(0, tk.END)

    selected_id = None


# ---------------- Select Record ----------------
def select_record(event):
    global selected_id

    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")

        clear()

        selected_id = values[0]

        entry_name.insert(0, values[1])
        entry_email.insert(0, values[2])
        entry_password.insert(0, values[3])


# ---------------- Update ----------------
def update_data():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Please Select a Record")
        return

    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if name == "" or email == "" or password == "":
        messagebox.showerror("Error", "All Fields Are Required")
        return

    sql = "UPDATE users SET name=%s,email=%s,password=%s WHERE id=%s"
    values = (name, email, password, selected_id)

    cursor.execute(sql, values)
    conn.commit()

    messagebox.showinfo("Success", "Record Updated Successfully")

    clear()
    show_data()


# ---------------- Delete ----------------
def delete_data():
    global selected_id

    if selected_id is None:
        messagebox.showerror("Error", "Please Select a Record")
        return

    result = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this record?"
    )

    if result:
        cursor.execute("DELETE FROM users WHERE id=%s", (selected_id,))
        conn.commit()

        messagebox.showinfo("Success", "Record Deleted Successfully")

        clear()
        show_data()


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Student Registration Form")
root.geometry("900x550")
root.configure(bg="lightblue")

title = tk.Label(
    root,
    text="Student Registration Form",
    font=("Arial", 18, "bold"),
    bg="lightblue",
    fg="blue"
)
title.pack(pady=10)

frame = tk.Frame(root, bg="white", bd=3, relief="groove")
frame.pack(pady=10)

tk.Label(frame, text="Name", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(frame, width=30, font=("Arial", 11))
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Email", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(frame, width=30, font=("Arial", 11))
entry_email.grid(row=1, column=1)

tk.Label(frame, text="Password", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0, padx=10, pady=10)
entry_password = tk.Entry(frame, width=30, show="*", font=("Arial", 11))
entry_password.grid(row=2, column=1)

# ---------------- Buttons ----------------
btn_frame = tk.Frame(root, bg="lightblue")
btn_frame.pack()

tk.Button(
    btn_frame,
    text="Register",
    command=register,
    bg="green",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12
).grid(row=0, column=0, padx=5)

tk.Button(
    btn_frame,
    text="Show Data",
    command=show_data,
    bg="blue",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12
).grid(row=0, column=1, padx=5)

tk.Button(
    btn_frame,
    text="Update",
    command=update_data,
    bg="purple",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12
).grid(row=0, column=2, padx=5)

tk.Button(
    btn_frame,
    text="Delete",
    command=delete_data,
    bg="red",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12
).grid(row=0, column=3, padx=5)

tk.Button(
    btn_frame,
    text="Clear",
    command=clear,
    bg="orange",
    fg="white",
    font=("Arial", 12, "bold"),
    width=12
).grid(row=0, column=4, padx=5)

# ---------------- Treeview ----------------
tree = ttk.Treeview(root)
tree["columns"] = ("ID", "Name", "Email", "Password")

tree.column("#0", width=0, stretch=tk.NO)
tree.column("ID", width=60, anchor="center")
tree.column("Name", width=180)
tree.column("Email", width=250)
tree.column("Password", width=180)

tree.heading("#0", text="")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Password", text="Password")

tree.pack(pady=20, fill="x")

tree.bind("<ButtonRelease-1>", select_record)

show_data()

root.mainloop()

cursor.close()
conn.close()