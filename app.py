import os
import sqlite3
import bcrypt
import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response

from database import get_db_connection, init_db

app = Flask(__name__)
app.secret_key = os.urandom(24) # Secure secret key for sessions

# Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Basic Validation
        if len(username) < 3 or len(password) < 6:
            flash('Username must be at least 3 characters and password at least 6 characters.', 'error')
            return render_template('register.html')
            
        # Hash password securely
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        conn = get_db_connection()
        c = conn.cursor()
        try:
            # Parameterized query to prevent SQL Injection
            c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed.decode('utf-8')))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            if user['is_2fa_enabled']:
                session['pending_user_id'] = user['id']
                return redirect(url_for('verify_2fa'))
            else:
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

@app.route('/setup_2fa', methods=['GET', 'POST'])
def setup_2fa():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT totp_secret, is_2fa_enabled FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if user['is_2fa_enabled']:
        conn.close()
        flash('2FA is already enabled.', 'info')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        token = request.form['token']
        secret = session.get('temp_totp_secret')
        if not secret:
            flash('Session expired. Try again.', 'error')
            return redirect(url_for('setup_2fa'))
            
        totp = pyotp.TOTP(secret)
        if totp.verify(token):
            c.execute('UPDATE users SET totp_secret = ?, is_2fa_enabled = 1 WHERE id = ?', (secret, user_id))
            conn.commit()
            flash('2FA successfully enabled!', 'success')
            session.pop('temp_totp_secret', None)
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid token. Try again.', 'error')
            conn.close()
            
    else:
        # Generate new secret if not already in session
        if 'temp_totp_secret' not in session:
            session['temp_totp_secret'] = pyotp.random_base32()
            
        secret = session['temp_totp_secret']
        totp = pyotp.TOTP(secret)
        prov_uri = totp.provisioning_uri(name=session['username'], issuer_name='SecureLoginApp')
        
        # Generate QR code
        img = qrcode.make(prov_uri)
        buf = BytesIO()
        img.save(buf, format='PNG')
        qr_b64 = b64encode(buf.getvalue()).decode('utf-8')
        conn.close()
        
        return render_template('setup_2fa.html', qr_b64=qr_b64, secret=secret)
        
    return render_template('setup_2fa.html')

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    if 'pending_user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        token = request.form['token']
        user_id = session['pending_user_id']
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT username, totp_secret FROM users WHERE id = ?', (user_id,))
        user = c.fetchone()
        conn.close()
        
        totp = pyotp.TOTP(user['totp_secret'])
        if totp.verify(token):
            session['user_id'] = user_id
            session['username'] = user['username']
            session.pop('pending_user_id', None)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid 2FA token.', 'error')
            
    return render_template('verify_2fa.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access the dashboard.', 'error')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT is_2fa_enabled FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    conn.close()
    
    return render_template('dashboard.html', username=session['username'], is_2fa_enabled=user['is_2fa_enabled'])

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('app.db'):
        init_db()
    app.run(debug=True, port=5000)
