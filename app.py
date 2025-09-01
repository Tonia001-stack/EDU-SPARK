import os
import requests
import bcrypt
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import uuid

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Get the secret key from the environment variable
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Check if the secret key was loaded successfully
if not app.secret_key:
    raise ValueError("No FLASK_SECRET_KEY found in .env file. Please set a unique and secret key.")

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tonia1' 
app.config['MYSQL_DB'] = 'eduspark'
mysql = MySQL(app)

# Get Paystack keys from environment variables
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")

# Hash password function
def hash_password(password):
    # Hash a password for the first time, with a salt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Check password function
def check_password(password, hashed_password):
    # Check a hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Strip any leading/trailing whitespace from the inputs
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        hashed_pw = hash_password(password)
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            mysql.connection.commit()
            return jsonify({'success': True, 'message': 'Registration successful! You can now log in.'})
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})
        finally:
            cursor.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Strip any leading/trailing whitespace from the inputs
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT id, username, password, is_premium FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and check_password(password, user[2]):
                session['loggedin'] = True
                session['id'] = user[0]
                session['username'] = user[1]
                session['is_premium'] = user[3]
                return jsonify({'success': True, 'message': 'Login successful!'})
            else:
                return jsonify({'success': False, 'message': 'Incorrect username or password.'})
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({'success': False, 'message': f'Database error: {str(e)}'})
        finally:
            cursor.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('is_premium', None)
    return redirect(url_for('home'))

@app.route('/lesson')
def free_lesson():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT title, content FROM lessons WHERE is_premium = FALSE ORDER BY id DESC LIMIT 1")
    lesson = cursor.fetchone()
    cursor.close()
    
    if lesson:
        return render_template('lesson.html', title=lesson[0], content=lesson[1])
    else:
        return render_template('lesson.html', title='No Lesson Available', content='Check back later for new content.')

@app.route('/premium')
def premium_quiz():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if session.get('is_premium'):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT title, content FROM lessons WHERE is_premium = TRUE ORDER BY id DESC LIMIT 1")
        quiz = cursor.fetchone()
        cursor.close()
        
        if quiz:
            return render_template('premium.html', title=quiz[0], content=quiz[1], has_access=True)
        else:
            return render_template('premium.html', title='No Quiz Available', content='Check back later.', has_access=True)
    else:
        return render_template('premium.html', title='Premium Quiz', content='Unlock this quiz by purchasing premium access!', has_access=False)

@app.route('/paystack-initiate', methods=['POST'])
def paystack_initiate():
    """Initiates a Paystack transaction and returns the authorization URL."""
    if 'loggedin' not in session:
        return jsonify({'success': False, 'message': 'User not logged in.'})

    user_email = request.form.get('email')
    
    # Paystack requires amount in kobo (NGN).
    # 10000 kobo is equivalent to ₦100.00
    amount_kobo = 10000
    
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": user_email,
        "amount": amount_kobo,
        "callback_url": url_for('verify_payment', _external=True)
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        if data['status']:
            return jsonify({
                'success': True,
                'authorization_url': data['data']['authorization_url']
            })
        else:
            return jsonify({'success': False, 'message': data['message']})

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'message': f'API error: {str(e)}'})

@app.route('/verify-payment')
def verify_payment():
    """Verifies a successful Paystack transaction."""
    trxref = request.args.get('trxref')

    if not trxref:
        return redirect(url_for('premium_quiz', message='Payment reference not found.'))

    url = f"https://api.paystack.co/transaction/verify/{trxref}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        if data['status'] and data['data']['status'] == 'success':
            user_id = session.get('id')
            if user_id:
                cursor = mysql.connection.cursor()
                try:
                    cursor.execute("UPDATE users SET is_premium = TRUE WHERE id = %s", (user_id,))
                    mysql.connection.commit()
                    session['is_premium'] = True
                    return redirect(url_for('premium_quiz', message='Payment successful! You now have premium access.'))
                except Exception as e:
                    mysql.connection.rollback()
                    return redirect(url_for('premium_quiz', message=f'Database error: {str(e)}'))
                finally:
                    cursor.close()
        else:
            return redirect(url_for('premium_quiz', message='Payment failed or was not successful.'))

    except requests.exceptions.RequestException as e:
        return redirect(url_for('premium_quiz', message=f'API error during verification: {str(e)}'))

    return redirect(url_for('premium_quiz', message='An unknown error occurred.'))

if __name__ == '__main__':
    app.run(debug=True)




