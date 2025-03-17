from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import json
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure you have a secret key for sessions

# Example data for passwords (this could be a database in a real app)
passwords_db = {}

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Ensure database and tables exist


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the contact form submission
        if 'name' in request.form and 'email' in request.form and 'message' in request.form:
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # For now, let's print the message to the console (you can send it to an email or store it in a database)
            print(f"New message from {name} ({email}): {message}")

            # Optionally, display a success message after form submission
            success_message = "Thank you for reaching out! We will get back to you soon."
            return render_template('index.html', success_message=success_message)
    
    return render_template('index.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password. Please try again."

    return render_template('login.html', error=error)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))  # Redirect to login after successful signup
        except sqlite3.IntegrityError:
            return "Username already taken. Please choose a different username."

    return render_template('signup.html')
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        if username in passwords_db and passwords_db[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        
        error = "Invalid username or password. Please try again."
    
    return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        if username in passwords_db:
            return "Username already taken. Please choose a different username."

        # Register new user by adding them to passwords_db
        passwords_db[username] = password
        return redirect(url_for('login'))  # Redirect to login after successful signup
    
    return render_template('signup.html')

'''
@app.route("/logout")
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for("index"))
'''
@app.route("/guest_login")
def guest_login():
    session["guest"] = True  # Set guest session
    print("Guest login successful. Session:", session)  # Debugging line
    return redirect(url_for("index"))  # Redirect to the home page after guest login'''

@app.route("/guest_login")
def guest_login():
    session["guest"] = True  # Set guest session
    print("Guest session set:", session)  # Debugging line
    return redirect(url_for("index"))  # Redirect to the home page after guest login



@app.route("/add_password", methods=["POST"])
def add_password():
    data = request.get_json()
    website = data.get("website")
    username = data.get("username")
    password = data.get("password")

    if website and username and password:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", (website, username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Password saved successfully!"})
    return jsonify({"message": "Failed to save password!"}), 400


@app.route("/search_password", methods=["POST"])
def search_password():
    data = request.get_json()
    website = data.get("website")

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE website = ?", (website,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"username": result[0], "password": result[1]})
    return jsonify({"message": "No password found!"}), 404


@app.route("/update_password", methods=["POST"])
def update_password():
    data = request.get_json()
    website = data.get("website")
    new_password = data.get("password")

    if not website or not new_password:
        return jsonify({"message": "Website and new password required!"}), 400

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET password = ? WHERE website = ?", (new_password, website))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "No password found for the given website!"}), 404

    conn.close()
    return jsonify({"message": "Password updated successfully!"})


@app.route("/delete_password", methods=["POST"])
def delete_password():
    data = request.get_json()
    website = data.get("website")

    if not website:
        return jsonify({"message": "Website required!"}), 400

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE website = ?", (website,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "No password found for the given website!"}), 404

    conn.close()
    return jsonify({"message": "Password deleted successfully!"})

@app.route('/show-passwords')
def show_passwords():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords")  # Change 'passwords' to your actual table name
    data = cursor.fetchall()
    conn.close()

    # Format results for CMD and Browser
    for row in data:
        print(row)  # This prints in CMD
    
    return "<br>".join([str(row) for row in data])  # Shows results in browser

if __name__ == "__main__":
    app.run(debug=True)
