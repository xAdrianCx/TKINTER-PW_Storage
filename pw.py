
import sqlite3
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


# Connect to SQLite3.
conn = sqlite3.connect('pw_storage.db')

# Check to see if connection to SQLite3 was created.
# print(conn)

# Create a cursor and initialize it.
my_cursor = conn.cursor()

# # Test if database was created.
# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#     print(db)

# # Drop/delete table.
# my_cursor.execute("DROP TABLE users")

# Create a table
my_cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user text,
	website text,
	email text,
	username text,
	password text)""")


# Query the database.
def query():
    # Create a database or connect to an existing one.
    conn = sqlite3.connect('pw_storage.db')
    my_cursor = conn.cursor()
    # Query the database
    my_cursor.execute("SELECT  rowid, * FROM users")
    records = my_cursor.fetchall()
    # Add database data to the treeview.
    global count
    count = 0
    for i in records:
        if count % 2 == 0:
            my_tree.insert(parent="", index="end", iid=count, text="",
                           values=(i[0], i[1], i[2], i[3], i[4], i[5]), tags=("evenrow",))
        else:
            my_tree.insert(parent="", index="end", iid=count, text="",
                           values=(i[0], i[1], i[2], i[3], i[4], i[5]), tags=("oddrow",))
        # increment counter.
        count += 1
    # Commit changes.
    conn.commit()
    # Close the connection to database.
    conn.close()


# Search through the database.
def search_box(event):
    # Add database data to the treeview.
    global count
    count = 0
    typed = search_entry.get()
    if typed != "":
        # Clear the treeview table.
        my_tree.delete(*my_tree.get_children())
        # Create a database or connect to an existing one.
        conn = sqlite3.connect('pw_storage.db')
        my_cursor = conn.cursor()
        # Query the database
        my_cursor.execute("SELECT  rowid, * FROM users")
        # Fetchall from database.
        records = my_cursor.fetchall()
        # Loop through the records and
        for x in records:
            if (typed.lower() in str(x[0]).lower()
                    or typed.lower() in str(x[1]).lower()
                    or typed.lower() in str(x[2]).lower()
                    or typed.lower() in str(x[3]).lower()
                    or typed.lower() in str(x[4]).lower()
                    or typed.lower() in str(x[5]).lower()):
                if count % 2 == 0:
                    my_tree.insert(parent="", index="end", iid=count, text="",
                                   values=(x[0], x[1], x[2], x[3], x[4], x[5]), tags=("evenrow",))
                else:
                    my_tree.insert(parent="", index="end", iid=count, text="",
                                   values=(x[0], x[1], x[2], x[3], x[4], x[5]), tags=("oddrow",))
                # increment counter.
                count += 1
        # Commit changes.
        conn.commit()
        # Close the connection to database.
        conn.close()
    else:
        # Clear the treeview table.
        my_tree.delete(*my_tree.get_children())
        # Create a database or connect to an existing one.
        conn = sqlite3.connect('pw_storage.db')
        my_cursor = conn.cursor()
        # Query the database
        my_cursor.execute("SELECT  rowid, * FROM users")
        # Fetchall from database.
        records = my_cursor.fetchall()
        # Add database data to the treeview.
        count = 0
        data = records
        for i in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="",
                               values=(i[0], i[1], i[2], i[3], i[4], i[5]), tags=("evenrow",))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="",
                               values=(i[0], i[1], i[2], i[3], i[4], i[5]), tags=("oddrow",))
            # increment counter.
            count += 1
        # Commit changes.
        conn.commit()
        # Close the connection to database.
        conn.close()


# # Show table.
# my_cursor.execute("SELECT * FROM users")
# # print(my_cursor.description)
# for i in my_cursor.description:
#     print(i)


# Get current working directory
cwd = os.getcwd()
root = Tk()
root.title('PW storage')
root.iconbitmap(os.path.join(cwd, 'images\\pw.ico'))
root.minsize(width=1000, height=600)
root.geometry('1000x600')
style = ttk.Style()
style.theme_use("default")

# Configure treeview color.
style.configure("Treeview",
                background= '#D3D3D3',
                foregriound= "black",
                rowheight=25,
                fieldbackground='#D3D3D3'
                )
style.map("Treeview",
          background=[('selected', '#347083')])

# Create a treeview frame.
tree_frame = Frame(root)
tree_frame.pack(fill="x", padx=20, pady=20)

# Create a treeview Scrollbar.
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create the Treeview and pack it on the screen.
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
my_tree.pack(fill="x")

# Configure the Scrollbar.
tree_scroll.config(command=my_tree.yview)

# Connect to SQLite3.
conn = sqlite3.connect('pw_storage.db')
my_cursor = conn.cursor()
# Define the columns of the treeview.
table = my_cursor.execute("SELECT * FROM users")
data = my_cursor.fetchall()

columns = ["ID"]
for i in range(0, len(table.description)):
    columns.append(table.description[i][0])
my_tree['columns'] = (columns)

# Format the columns.
my_tree.column("#0", width=0, stretch=NO)
for i in range(0, len(table.description)):
    my_tree.column(table.description[i][0], anchor=W, width=140)

# Create the headings.
my_tree.heading("#0", text="", anchor=W)
for i in range(0, len(columns)):
    my_tree.heading(columns[i], text=str(columns[i]).upper(), anchor=W)

# Create striped row tags.
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


# Select a record.
def select_record(event):
    # Clear entry boxes.
    clear_boxes()
    # Get the selected item from a treeview.
    selected = my_tree.focus()
    # Get the record values.
    values = my_tree.item(selected, 'values')
    # After a record is selected on the treeview, show the values in entry boxes.
    str_id.set(values[0])
    user_entry.insert(0, values[1])
    website_entry.insert(0, values[2])
    email_entry.insert(0, values[3])
    username_entry.insert(0, values[4])
    pw_entry.insert(0, values[5])


# Update a record.
def update_record():
    # Get the record number.
    selected = my_tree.focus()
    # Update record.
    my_tree.item(selected, text="", values=(
        id_entry.get(),
        user_entry.get(),
        website_entry.get(),
        email_entry.get(),
        username_entry.get(),
        pw_entry.get(),))
    # Create a database or connect to an existing one.
    conn = sqlite3.connect('pw_storage.db')
    my_cursor = conn.cursor()
    my_cursor.execute("""UPDATE users SET 
      user = :user,
      website = :website,
      email = :email,
      username = :username,
      password = :password
      
      WHERE oid = :oid""",
                      {
                        'user': user_entry.get(),
                        'website': website_entry.get(),
                        'email': email_entry.get(),
                        'username': username_entry.get(),
                        'password': pw_entry.get(),
                        'oid': id_entry.get()
                        })
    # Commit changes.
    conn.commit()
    # Close the connection to database.
    conn.close()
    clear_boxes()
    # Add a message after updating the database.
    messagebox.showinfo("Updated!", "Selected record has been updated!")


# Add a new record to the database.
def add_new_record():
    # Create a database or connect to an existing one.
    conn = sqlite3.connect('pw_storage.db')
    my_cursor = conn.cursor()
    # Add new record.
    my_cursor.execute("INSERT INTO users VALUES (:user, :website, :email, :username, :password)",
                      {
                          'user': user_entry.get(),
                          'website': website_entry.get(),
                          'email': email_entry.get(),
                          'username': username_entry.get(),
                          'password': pw_entry.get()
                      })
    my_cursor.execute("SELECT * from users")
    # Commit changes.
    conn.commit()
    # Close the connection to database.
    conn.close()
    # Show a message if the action completed successfully.
    messagebox.showinfo("Added New Record!", "A new record has been added to the database!")
    # Clear entry boxes.
    clear_boxes()
    # Clear the treeview table.
    my_tree.delete(*my_tree.get_children())
    # Query the database again to see the changes.
    query()


# Clear the boxes.
def clear_boxes():
    # Clear entry boxes.
    str_id.set("")
    user_entry.delete(0, END)
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    username_entry.delete(0, END)
    pw_entry.delete(0, END)


# Remove records.
def remove_selected_records():
    response = messagebox.askyesno("Warning!!!", "This will remove selected records from the database. Are you sure?")
    if response == 1:
        # Get the record(s) we want to delete.
        selected = my_tree.selection()
        # Add the record(s) we want to delete to a list.
        to_delete = []
        # Add selected record(s) to the deletion list.
        for record in selected:
            to_delete.append(my_tree.item(record, 'values')[0])
        # Create a database or connect to an existing one.
        conn = sqlite3.connect('pw_storage.db')
        my_cursor = conn.cursor()
        my_cursor.executemany("DELETE FROM users WHERE oid= ?", [(a,) for a in to_delete])
        # Commit changes.
        conn.commit()
        # Close the connection to database.
        conn.close()
        # Show a message if the action completed successfully.
        messagebox.showinfo("Deleted!", "Selected records have been deleted from the database!")
        # Clear entry boxes.
        clear_boxes()
        # Clear the treeview table.
        my_tree.delete(*my_tree.get_children())
        # Query the database again to see the changes.
        query()


def remove_all_records():
    response = messagebox.askyesno("Warning!!!", "This will remove selected records from the database. Are you sure?")
    if response == 1:
        for record in my_tree.get_children():
            my_tree.delete(record)
        # Create a database or connect to an existing one.
        conn = sqlite3.connect('pw_storage.db')
        my_cursor = conn.cursor()
        # Delete everything from the database.
        my_cursor.execute("DROP TABLE users")
        # Commit changes.
        conn.commit()
        # Close the connection to database.
        conn.close()
        # Show a message if the action completed successfully.
        messagebox.showinfo("Deleted!", "All records have been deleted from the database! You need to restart the application!")
        # Clear entry boxes.
        clear_boxes()
        root.destroy()
    else:
        pass


# Add record Entry Boxes.
data_frame = LabelFrame(root, text="Selected Record")
data_frame.pack(fill="x", padx=20)

# Set a string variable for the id just to be able to make it unchangeable by user.
# It changes from select_record() function.
str_id = StringVar()
id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame, textvariable=str_id, state=DISABLED)
id_entry.grid(row=0, column=1, padx=10, pady=10)

# Create a user label and entry box.
user_label = Label(data_frame, text="User")
user_label.grid(row=0, column=2, padx=10, pady=10)
user_entry = Entry(data_frame)
user_entry.grid(row=0, column=3, padx=10, pady=10)

# Create a website label and entry box.
website_label = Label(data_frame, text="Website")
website_label.grid(row=0, column=4, padx=10, pady=10)
website_entry = Entry(data_frame)
website_entry.grid(row=0, column=5, padx=10, pady=10)

# Create an email label and entry box.
email_label = Label(data_frame, text="Email")
email_label.grid(row=0, column=6, padx=10, pady=10)
email_entry = Entry(data_frame)
email_entry.grid(row=0, column=7, padx=10, pady=10)

# Create a username label and entry box.
username_label = Label(data_frame, text="Username")
username_label.grid(row=1, column=0, padx=10, pady=10)
username_entry = Entry(data_frame)
username_entry.grid(row=1, column=1, padx=10, pady=10)

# Create a pw label and entry box.
pw_label = Label(data_frame, text="Password")
pw_label.grid(row=1, column=2, padx=10, pady=10)
pw_entry = Entry(data_frame)
pw_entry.grid(row=1, column=3, padx=10, pady=10)

# Add buttons.
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", padx=20, pady=20)

# Update button
update_button = Button(button_frame, text="Update Record", command=update_record).grid(row=0, column=0, padx=20, pady=20)
# Add button.
add_button = Button(button_frame, text="Add New Record", command=add_new_record).grid(row=0, column=1, padx=20, pady=20)
# Remove selected record button.
remove_selected_button = Button(button_frame, text="Remove Selected Records", command=remove_selected_records).grid(row=0, column=2, padx=20, pady=20)
# Remove all records button.
remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all_records).grid(row=0, column=3, padx=20, pady=20)
# Clear boxes.
clear_boxes_button = Button(button_frame, text="Clear Boxes", command=clear_boxes).grid(row=0, column=4, padx=20, pady=20)
# Create asearch label and entry box.
search_label = Label(button_frame, text="Search...")
search_label.grid(row=0, column=5, padx=10, pady=10)
search_entry = Entry(button_frame)
search_entry.grid(row=0, column=6, padx=10, pady=10)

# Bind the treeview to selected_record function.
my_tree.bind("<ButtonRelease-1>", select_record)
# Bind the search entry box.
search_entry.bind("<KeyRelease>", search_box)

# Query the database at startup.
query()
# Commit and close the database.
conn.commit()
conn.close()
root.mainloop()