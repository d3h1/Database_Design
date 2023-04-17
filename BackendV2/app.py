from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db_path = 'phase1.sqlite'

app.config['FLASH_CATEGORY'] = 'now'

def init_database():
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        email TEXT,
                        firstName TEXT,
                        lastName TEXT,
                        password TEXT
                        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS items (
                        username TEXT,
                        title TEXT,
                        description TEXT,
                        category TEXT,
                        price REAL,
                        date TEXT
                        )''')
        
        # Add example users
        example_users = [
            ('user1', 'email1@gmail.com','first1','last1', 'password1'),
            ('user2', 'email2@gmail.com','first2','last2', 'password2'),
            ('user3', 'email3@gmail.com','first3','last3', 'password3'),
            ('user4', 'email4@gmail.com','first4','last4', 'password4'),
            ('user5', 'email5@gmail.com','first5','last5', 'password5'),
        ]

        conn.executemany('''
        INSERT INTO users (username, email, firstName, lastName, password) VALUES (?, ?, ?, ?, ?);
        ''', example_users)
        
        
        conn.commit()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'signin':
            return handle_signin()
        elif action == 'signup':
            return redirect(url_for('handle_signup'))
        elif action == 'init_db':
            init_database()
            flash('Database initialize successfully!', app.config['FLASH_CATEGORY'])
    return render_template('signin.html')

@app.route('/add_item', methods=['GET','POST'])
def add_item():
    if request.method == 'POST':
        
        username = request.form['username']
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        today = date.today()
    
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO items (username, title, description, category, price, date) VALUES (?, ?, ?, ?, ?, ?)''', (username, title, description, category, price, today))
            conn.commit()
            
            flash('Item added successfully!', app.config['FLASH_CATEGORY'])
    return render_template('searchbar.html')

@app.route('/signin', methods=['GET', 'POST'])
def handle_signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            user = c.fetchone()
            if user is None:
                flash('Invalid username or password!', app.config['FLASH_CATEGORY'])
            else:
                flash('Sign in successful!', app.config['FLASH_CATEGORY'])
                return redirect(url_for('profile', firstName=user[2], lastName=user[3]))
    return render_template('signin.html')


@app.route('/profile/<firstName>/<lastName>')
def profile(firstName, lastName):
    return render_template('profile.html', name=firstName + " " + lastName)


@app.route('/signup', methods=['GET', 'POST'])
def handle_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()

            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            if c.fetchall():
                flash('Username already exists!', app.config['FLASH_CATEGORY'])
                return redirect(url_for('handle_signup'))

            c.execute('SELECT * FROM users WHERE email = ?', (email,))
            if c.fetchall():
                flash('Email already exists!', app.config['FLASH_CATEGORY'])
                return redirect(url_for('handle_signup'))

            if password != confirmPassword:
                flash('Passwords do not match!', 'danger', app.config['FLASH_CATEGORY'])
                return redirect(url_for('handle_signup'))

            c.execute('''INSERT INTO users (username, email, firstName, lastName, password) 
                          VALUES (?, ?, ?, ?, ?)''', (username, email, firstName, lastName, password))
            conn.commit()

            flash('Registration successful!', app.config['FLASH_CATEGORY'])
            return redirect(url_for('handle_signin'))

    return render_template('signup.html')



@app.route('/searchbar', methods=['GET', 'POST'])
def searchbar():
    return render_template('searchbar.html')


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
