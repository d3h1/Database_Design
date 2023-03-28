# We are creating a python application that uses certain GUI builders to create a login / registration page that connects directly to an sql database. 

# Youtube link
    https://www.youtube.com/watch?v=yNvEfQz4tw8

# FOR PYTHON -- PHASE 1
We might need to install 2 libraries || usually standard libraries in python now
## IMPORTS NEEDED
    pip install tkinter
    pip install sqlite3
    import os
    import runpy
    

Then we will import and create the code around that.

### For phase one, frontend + flask is not needed, but we can and will create a front end portion connecting our python / sql using a basic flask REST API


# PREVENTING SQL INJECTION ATTACKS
    1. We were able to do this by using parameterized querying in our c.execute() method.
    2. We use '?' as the placeholder in order to represent values like username and password
    3. In the register page, we also use a modified 'INSERT' statement. 

# INITIALIZATION DATABASE BUTTON
    1. By pressing hte button in the main GUI.PY, user is able to initialize a database
    2. The login and signup should access that database to make their usernames, etc