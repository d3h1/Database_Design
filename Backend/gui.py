import tkinter as tk
import os

# Create the tkinter window
root = tk.Tk()
root.title('Login/Registration')

# Create the login button
login_button = tk.Button(root, text='Login', command=lambda: os.system('python Backend\signin.py'))
login_button.grid(row=0, column=0, padx=5, pady=5)

# Create the register button
register_button = tk.Button(root, text='Register', command=lambda: os.system('python Backend\signup.py'))
register_button.grid(row=0, column=1, padx=5, pady=5)

# Run the tkinter main loop
root.mainloop()
