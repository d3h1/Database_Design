import tkinter as tk
import sqlite3
import os

# Connect to the database
conn = sqlite3.connect('testing.sqlite')
c = conn.cursor()

# Create the user table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS users (
             username TEXT PRIMARY KEY,
             email TEXT,
             firstName TEXT,
             lastName TEXT,
             password TEXT
             )''')

# Create the register function
def register():
    # Get the user information
    username = username_entry.get()
    email = email_entry.get()
    firstName = firstName_entry.get()
    lastName = lastName_entry.get()
    password = password_entry.get()
    confirmPassword = confirmPassword_entry.get()
    
    # Check if the username already exists
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    if c.fetchone() is not None:
        # Username already exists
        register_label.config(text='Username already exists!', fg='red')
        return
    
    # Check if the email already exists
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    if c.fetchone() is not None:
        # Email already exists
        register_label.config(text='Email already exists!', fg='red')
        return
    
    # Check if the passwords match
    if password != confirmPassword:
        # Passwords do not match
        register_label.config(text='Passwords do not match!', fg='red')
        return
    
    # Insert the new user into the database
    try:
        c.execute('INSERT INTO users (username, email, firstName, lastName, password) VALUES (?, ?, ?, ?, ?)',
                  (username, email, firstName, lastName, password))
        conn.commit()
    except sqlite3.IntegrityError:
        # Failed to insert user
        register_label.config(text='Registration failed!', fg='red')
        return
        
    # Registration successful
    register_label.config(text='Registration successful!', fg='green')
    
    # Launch gui.py
    os.system("python Backend/gui.py")


# Create the tkinter window
root = tk.Tk()
root.title('Registration')

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

# Create the confirm password label and entry
confirmPassword_label = tk.Label(root, text='Confirm Password:')
confirmPassword_label.grid(row=2, column=0, padx=5, pady=5)
confirmPassword_entry = tk.Entry(root, show='*')
confirmPassword_entry.grid(row=2, column=1, padx=5, pady=5)

# Create the first name label and entry
firstName_label = tk.Label(root, text='First Name:')
firstName_label.grid(row=3, column=0, padx=5, pady=5)
firstName_entry = tk.Entry(root)
firstName_entry.grid(row=3, column=1, padx=5, pady=5)

# Create the last name label and entry
lastName_label = tk.Label(root, text='Last Name:')
lastName_label.grid(row=4, column=0, padx=5, pady=5)
lastName_entry = tk.Entry(root)
lastName_entry.grid(row=4, column=1, padx=5, pady=5)

# Create the email label and entry
email_label = tk.Label(root, text='Email:')
email_label.grid(row=5, column=0, padx=5, pady=5)
email_entry = tk.Entry(root)
email_entry.grid(row=5, column=1, padx=5, pady=5)

# Create the register button
register_button = tk.Button(root, text='Register', command=register)
register_button.grid(row=6, column=0, padx=5, pady=5)

# Create the register label
register_label = tk.Label(root, text='')
register_label.grid(row=7, column=1, padx=5, pady=5)

# Run the tkinter main loop
root.mainloop()
