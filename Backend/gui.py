# Imports needed
import tkinter as tk
import sqlite3
import os
import runpy

# Create the tkinter window
root = tk.Tk()
root.title('Phase 1!')

# Configure the window size and background color
root.geometry('380x150')
root.configure(bg='#C6DEF1')


def find_project_root():
    current_folder = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(current_folder, "Backend")):
        current_folder = os.path.abspath(os.path.join(current_folder, os.pardir))
        if os.path.splitdrive(current_folder)[1] == '\\':
            raise FileNotFoundError("Could not find the project root folder")
    return current_folder

# Finding project root folder to collect the absolute paths
project_root = find_project_root()
signin_path = os.path.join(project_root, 'Backend', 'signin.py')
signup_path = os.path.join(project_root, 'Backend', 'signup.py')

# ! DEBUGGING PATHS
# print("Signin path:", signin_path)
# print("Signup path:", signup_path)

# We use runpy to run our paths and scripts in each of them
def run_script(script_path, db_path=None):
    script_directory = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)
    
    # Change the working directory temporarily
    original_cwd = os.getcwd()
    os.chdir(script_directory)
    
    # Set the environment variable for the database path
    if db_path is not None:
        os.environ['DB_PATH'] = db_path
    else: 
        raise ValueError("Database was not provided")
    
    # Run the script
    try:
        runpy.run_path(script_path)
    finally:
        # Restore the original working directory
        os.chdir(original_cwd)

def init_database(db_path):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        # Add any additional code to initialize the database here
        conn.close()

# Creating the path to the DB that we initialize
db_path = os.path.join(project_root, 'phase1.sqlite')

# Create a label with the title
title_label = tk.Label(root, text='Welcome!', font=('Arial', 20, 'bold'), bg='#C6DEF1')
title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Create the login button
login_button = tk.Button(root, text='Login', font=('Arial', 14), command=lambda: run_script(signin_path, db_path=db_path))
login_button.grid(row=1, column=0, padx=10, pady=10)

# Create init button
init_button = tk.Button(root, text='Initialize Database', font=('Arial', 14), command=lambda: init_database(db_path))
init_button.grid(row=1, column=1, padx=10, pady=10)

# Create the register button
register_button = tk.Button(root, text='Register', font=('Arial', 14), command=lambda: run_script(signup_path, db_path=db_path))
register_button.grid(row=1, column=2, padx=10, pady=10)


# Run the tkinter main loop
root.mainloop()
