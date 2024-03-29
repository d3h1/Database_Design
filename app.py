from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session, make_response
import sqlite3
import os
from datetime import datetime, timedelta
import json

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
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        title TEXT,
                        description TEXT,
                        category TEXT,
                        price REAL,
                        date TEXT
                        )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    item_id INTEGER,
                    rating TEXT,
                    description TEXT,
                    date TEXT
                    )''')
        
        conn.execute('''CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    favorite_user TEXT NOT NULL
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


@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            # Check if the username exists in the user table
            c.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            count = c.fetchone()[0]
            if count > 0:
                c.execute('SELECT COUNT(*) FROM items WHERE username = ? AND date BETWEEN ? AND ?', (username, yesterday, today))
                count = c.fetchone()[0]
                if count < 3:
                    c.execute('INSERT INTO items (username, title, description, category, price, date) VALUES (?, ?, ?, ?, ?, ?)', (username, title, description, category, price, today))
                    conn.commit()
                    flash('Item added successfully!', app.config['FLASH_CATEGORY'])
                    return render_template('searchbar.html')
                else:
                    flash('You have reached the maximum limit of 3 posts in a day', app.config['FLASH_CATEGORY'])
                    return render_template('searchbar.html')
            else:
                flash('Invalid username. Please enter a valid username.', app.config['FLASH_CATEGORY'])
                return render_template('searchbar.html')
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
                response = make_response(redirect(url_for('profile',username=user[0], email=user[1], firstName=user[2], lastName=user[3])))
                response.set_cookie('username', user[0])
                return response
                
    return render_template('signin.html')


@app.route('/profile/<firstName>/<lastName>/<username>/<email>')
def profile(firstName, lastName, username, email):    
    return render_template('profile.html', name=firstName + " " + lastName, username=username, email=email) 


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
                flash('Passwords do not match!', app.config['FLASH_CATEGORY'])
                return redirect(url_for('handle_signup'))

            c.execute('''INSERT INTO users (username, email, firstName, lastName, password) 
                        VALUES (?, ?, ?, ?, ?)''', (username, email, firstName, lastName, password))
            conn.commit()

            flash('Registration successful!', app.config['FLASH_CATEGORY'])
            return redirect(url_for('handle_signin'))
    return render_template('signup.html')

@app.route('/add_favorite', methods=['GET', 'POST'])
def add_favorite():
    if request.method == 'POST':
        username = request.form['username']
        favorite_user = request.form['favorite_user']
        next_url = request.form.get('next')

        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO favorites (username, favorite_user) VALUES (?, ?)', (username, favorite_user))
            conn.commit()

        flash('Favorite added successfully!', app.config['FLASH_CATEGORY'])

        if next_url:
            return redirect(next_url)
        else:
            return redirect(url_for('searchbar'))

    return render_template('searchbar.html')


@app.route('/searchbar', methods=['GET', 'POST'])
def searchbar():
    if request.method == 'GET':
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT DISTINCT category FROM items')
            categories = [row[0] for row in c.fetchall()]
            return render_template('searchbar.html', categories=categories)
    elif request.method == 'POST':
        selected_item_id = request.form.get('selected_item_id')
        if selected_item_id:
            # retrieve the selected item from the database and pass it to the selected.html template
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute('SELECT * FROM items WHERE id = ?', (selected_item_id))
                item = c.fetchone()
                if item:
                    return render_template('selected.html', item=item)
        # if no item was selected, just render the searchbar template
        return redirect(url_for('searchbar'))


@app.route('/searchusers', methods=['GET'])
def searchusers():
    print(request.args.get('query', None))
    if request.args.get('query'):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''SELECT DISTINCT username FROM items WHERE username NOT IN (SELECT DISTINCT username FROM items WHERE rating = "Poor")''')
            item = c.fetchall()
            print(item)
    return render_template('searchusers.html')

# PHASE 3 - Tasks
@app.route('/marketplace', methods = ['GET', 'POST'])
def marketplace():
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            # Fetch all items from the database
            c.execute('SELECT * FROM items')
            items = c.fetchall()
        
        # (TASK 1)
        # Fetch most expensive items 
        c.execute('SELECT *, MAX(price) as max_prices FROM items GROUP by category')
        max_prices = c.fetchall()
        
        # !(TASK 2)
        # Get the two categories entered by the user
        category1 = request.args.get('category1')
        category2 = request.args.get('category2')
        
        # !(TASK 2)
        # Search for the user who has both categories 
        c.execute('SELECT DISTINCT username FROM items WHERE category=? OR category=? GROUP BY username HAVING COUNT(DISTINCT category) = 2', (category1, category2))
        users = c.fetchall()
        
        # !(TASK 3)
        # Get the username entered by the user 
        username = request.args.get('username')
        
        # (TASK 3 - modified)
        # Fetch all items posted by the given username that have received only "Excellent" or "Great" reviews
        c.execute('SELECT i.id, i.username, i.title, i.description, i.category, i.price, r.rating, r.date FROM items i JOIN reviews r ON i.id = r.item_id WHERE i.username=? AND r.rating IN ("Excellent", "Great") GROUP BY i.id HAVING COUNT(*) = SUM(CASE WHEN r.rating IN ("Excellent", "Great") THEN 1 ELSE 0 END)', (username,))
        items = c.fetchall()

        # Display the items in an HTML table
        if items:
            html = '<table>'
            html += '<tr><th>Title</th><th>Description</th><th>Category</th><th>Price</th><th>Rating</th><th>Review Date</th></tr>'
            for item in items:
                html += '<tr>'
                html += '<td>' + item[2] + '</td>'
                html += '<td>' + item[3] + '</td>'
                html += '<td>' + item[4] + '</td>'
                html += '<td>$' + str(item[5]) + '</td>'
                html += '<td>' + item[6] + '</td>'
                html += '<td>' + item[7] + '</td>'
                html += '</tr>'
            html += '</table>'
        else:
            html = 'No items found'
        
        # !(TASK 4)
        # List the users who posted the most number of items since 5/1/2020 (inclusive) 
        c.execute('''
                    SELECT username, COUNT(*) as num_items
                    FROM items
                    WHERE date >= "2020-05-01"
                    GROUP BY username
                    HAVING num_items = (
                        SELECT COUNT(*)
                        FROM items
                        WHERE date >= "2020-05-01"
                        GROUP BY username
                        ORDER BY COUNT(*) DESC
                        LIMIT 1
            )
    ''')
        top_users = c.fetchall()
        
        # !(TASK 5)
        # Fetch all usernames from the database and display them in a dropdown menu
        c.execute('SELECT DISTINCT username FROM favorites')
        usernames = c.fetchall()

        # Check if both dropdown menus are selected and find the users who have the same favorite user
        if request.method == 'POST':
            username1 = request.form['username1']
            username2 = request.form['username2']
            c.execute('''SELECT DISTINCT favorite_user FROM favorites WHERE username=? AND favorite_user IN 
                        (SELECT favorite_user FROM favorites WHERE username=?)''', (username1, username2))
            common_favorites = c.fetchall()
        else:
            common_favorites = None
            
        # !(TASK 6)
        # Display all the users who never posted any "excellent" items where excellent is any item with at least three excellent reviews
        c.execute('''
            SELECT DISTINCT items.username
            FROM items
            LEFT JOIN (
                SELECT item_id
                FROM reviews
                WHERE rating = 'Excellent'
                GROUP BY item_id
                HAVING COUNT(*) >= 3
            ) e ON items.id = e.item_id
            LEFT JOIN reviews r ON items.id = r.item_id
            WHERE e.item_id IS NULL OR r.rating != 'Excellent';
        ''')
        excellent_users = c.fetchall()
        
        # !(TASK 7)
        # Fetch all usernames from the database that have never rated something 'poor'
        c.execute('''
            SELECT DISTINCT username
            FROM reviews
            WHERE username NOT IN (
                SELECT DISTINCT username
                FROM reviews
                WHERE rating = "Poor"
            )
        ''')
        users2= c.fetchall()
        
        # !(TASK 8)
        # Display all the users who posted reviews with only ratings of "Poor"
        c.execute('''SELECT DISTINCT username 
                    FROM reviews 
                    WHERE username NOT IN (
                        SELECT DISTINCT username 
                        FROM reviews 
                        WHERE rating != "Poor"
                        AND username IN (
                            SELECT DISTINCT username 
                            FROM reviews 
                            WHERE rating != "Poor"
                        )
                    )''')
        poor_review_users = c.fetchall()
        
        # !(TASK 9)
        # Display users such that each item they posted so far never received any "Poor" reviews
        c.execute('''
            WITH poor_review_users AS (
                SELECT DISTINCT i.username
                FROM items i
                JOIN reviews r ON i.id = r.item_id
                WHERE r.rating = "Poor"
            )
            SELECT DISTINCT i.username
            FROM items i
            WHERE i.username NOT IN (SELECT username FROM poor_review_users)
        ''')
        good_item_users = c.fetchall()

        
        # !(TASK 10)
        # Get a user pair (A, B) such that they always gave each other "excellent" reviews for every single item they posted
        c.execute('''SELECT i1.username as user1, i2.username as user2
                    FROM items i1
                    INNER JOIN reviews r1 ON i1.id = r1.item_id AND r1.rating = 'Excellent'
                    INNER JOIN items i2 ON i2.username = r1.username AND i1.id != i2.id
                    INNER JOIN reviews r2 ON i2.id = r2.item_id AND r2.username = i1.username
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM reviews r3
                        WHERE r3.username = i1.username AND r3.item_id = i2.id AND r3.rating != 'Excellent'
                        OR r3.username = i2.username AND r3.item_id = i1.id AND r3.rating != 'Excellent'
                    )''')
        excellent_review_pairs = [list(sorted(x)) for x in c.fetchall()]
        ret = [pair for i, pair in enumerate(excellent_review_pairs) if pair not in excellent_review_pairs[:i]]


    
        return render_template('marketplace.html', item_results=items, max_prices=max_prices, users=users, users2=users2, items=items, top_users=top_users, excellent_users=excellent_users, poor_review_users=poor_review_users, good_item_users=good_item_users, excellent_review_pairs=ret, common_favorites=common_favorites, usernames=usernames, )



@app.route('/search_items', methods=['GET'])
def search_items():
    if request.method == 'GET':
        category = request.args.get('category')
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM items WHERE category = ?', (category,))
            items = c.fetchall()
            return render_template('searchbar.html', search_results=items)
    return redirect(url_for('searchbar'))


@app.route('/item/<int:item_id>/')
def item_detail(item_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        item = c.fetchone()
        if item:
            c.execute('SELECT * FROM reviews WHERE item_id = ?', (item_id,))
            reviews = c.fetchall()
            return render_template('selected.html', item=item, reviews=reviews)
        else:
            return "Item not found", 404


@app.route('/item/<int:item_id>/submit_review', methods=['GET','POST'])
def submit_review(item_id):
    if request.method == 'POST':
        username = request.form['username']
        rating = request.form['rating']
        description = request.form['description']
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            # Check if the username exists in the user table
            c.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            user_count = c.fetchone()[0]
            if user_count == 0:
                flash('You must be a registered user to submit a review', app.config['FLASH_CATEGORY'])
                return redirect(url_for('item_detail', item_id=item_id))
            # Retrieve the username associated with the item_id
            c.execute('SELECT username FROM items WHERE id = ?', (item_id,))
            item_username = c.fetchone()[0]
            if username == item_username:
                flash('You cannot review your own product', app.config['FLASH_CATEGORY'])
                return redirect(url_for('item_detail', item_id=item_id))
            c.execute('SELECT COUNT(*) FROM reviews WHERE username = ? AND date BETWEEN ? AND ?', (username, yesterday, today))
            count = c.fetchone()[0]
            if count < 3:
                c.execute('INSERT INTO reviews (username, item_id, rating, description, date) VALUES (?, ?, ?, ?, ?)', (username, item_id, rating, description, today))
                conn.commit()
                flash('Review submitted successfully!', app.config['FLASH_CATEGORY'])
                return redirect(url_for('item_detail', item_id=item_id))
            else: 
                flash('You have reached the maximum limit of 3 reviews in a day', app.config['FLASH_CATEGORY'])
            return redirect(url_for('item_detail', item_id=item_id))
    return render_template('selected.html')
 

@app.route('/clear-flash', methods=['POST'])
def clear_flash():
    session.pop('_flashes', None)
    return '', 204


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
