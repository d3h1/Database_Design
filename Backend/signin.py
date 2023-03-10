import tkinter as tk
import sqlite3

# Connect to the database
conn = sqlite3.connect('testing.sqlite')
c = conn.cursor()

# Create the tkinter window
root = tk.Tk()
root.title('Sign In')

# Create the username label and entry
username_label = tk.Label(root, text='Username:')
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

# Create the password label and entry
password_label = tk.Label(root, text='Password:')
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show='*')
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Create the sign in function
def sign_in():
    # Get the user information
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password match a user in the database
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    if user is None:
        # Username and password do not match a user in the database
        sign_in_label.config(text='Invalid username or password!', fg='red')
    else:
        # Username and password match a user in the database
        sign_in_label.config(text='Sign in successful!', fg='green')

# Create the sign in button
sign_in_button = tk.Button(root, text='Sign In', command=sign_in)
sign_in_button.grid(row=2, column=0, padx=5, pady=5)

# Create the sign in label
sign_in_label = tk.Label(root, text='')
sign_in_label.grid(row=2, column=1, padx=5, pady=5)

# Run the tkinter main loop
root.mainloop()