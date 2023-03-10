import tkinter as tk
import os

# Create the tkinter window
root = tk.Tk()
root.title('Phase 1!')

# Configure the window size and background color
root.geometry('190x150')
root.configure(bg='#C6DEF1')

# Create a label with the title
title_label = tk.Label(root, text='Welcome!', font=('Arial', 20, 'bold'), bg='#C6DEF1')
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create the login button
login_button = tk.Button(root, text='Login', font=('Arial', 14), command=lambda: os.system('python Backend\signin.py'))
login_button.grid(row=1, column=0, padx=10, pady=10)

# Create the register button
register_button = tk.Button(root, text='Register', font=('Arial', 14), command=lambda: os.system('python Backend\signup.py'))
register_button.grid(row=1, column=1, padx=10, pady=10)

# Run the tkinter main loop
root.mainloop()
