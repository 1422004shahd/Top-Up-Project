# from flask import Flask, request, jsonify, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)

# # Configure mydb2
# app.config['SQLALCHEMY_mydb2_URI'] = 'sqlite:///mydb2.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# # Initialize mydb2
# with app.app_context():
#     db.create_all()

# @app.route('/')
# def home():
#     return "Welcome to the Login System"

# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     if not username or not email or not password:
#         return jsonify({"error": "All fields are required"}), 400

#     hashed_password = generate_password_hash(password, method='sha256')
#     new_user = User(username=username, email=email, password=hashed_password)

#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify({"message": "User registered successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": "User already exists"}), 400

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')

#     if not email or not password:
#         return jsonify({"error": "Email and password are required"}), 400

#     user = User.query.filter_by(email=email).first()
#     if user and check_password_hash(user.password, password):
#         return jsonify({"message": "Login successful"}), 200
#     else:
#         return jsonify({"error": "Invalid credentials"}), 401

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# SQLite database path
DATABASE = 'mydb2.db'

# Helper function to interact with the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This helps return rows as dictionaries
    return conn

# Route to serve the index.html (this is where the form is)
@app.route('/')
def index():
    return render_template('index.html')

# Registration route to handle form submission
@app.route('/register', methods=['POST'])
def register():
    # Extract the JSON data from the request body
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required!'}), 400

    # Save the new user in the database
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Create users table if not exists (check if table exists or create it)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           email TEXT NOT NULL UNIQUE,
                           password TEXT NOT NULL)''')
        
        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, password))
        conn.commit()
        conn.close()

        # Confirm the success
        return jsonify({'message': 'Registration successful!'}), 200
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
