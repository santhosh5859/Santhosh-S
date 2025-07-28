from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('security_portal.db')
    cursor = conn.cursor()
    
    # Guards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            badge_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Visitor entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitor_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guard_id INTEGER NOT NULL,
            visitor_name TEXT NOT NULL,
            visitor_image TEXT,
            purpose_of_visit TEXT NOT NULL,
            checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            checkout_time TIMESTAMP,
            visitor_signature TEXT,
            status TEXT DEFAULT 'checked_in',
            FOREIGN KEY (guard_id) REFERENCES guards (id)
        )
    ''')
    
    # Duty logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS duty_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guard_id INTEGER NOT NULL,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            logout_time TIMESTAMP,
            duration_minutes INTEGER,
            FOREIGN KEY (guard_id) REFERENCES guards (id)
        )
    ''')
    
    # Seed default test account
    test_password_hash = generate_password_hash('0987')
    cursor.execute('''
        INSERT OR IGNORE INTO guards (full_name, badge_id, password_hash)
        VALUES (?, ?, ?)
    ''', ('Sany S', '1234', test_password_hash))
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('security_portal.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Landing page - redirect to login if not authenticated"""
    if 'guard_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Guard login page"""
    if request.method == 'POST':
        badge_id = request.form['badge_id']
        password = request.form['password']
        
        conn = get_db_connection()
        guard = conn.execute(
            'SELECT * FROM guards WHERE badge_id = ?', (badge_id,)
        ).fetchone()
        
        if guard and check_password_hash(guard['password_hash'], password):
            session['guard_id'] = guard['id']
            session['guard_name'] = guard['full_name']
            session['badge_id'] = guard['badge_id']
            
            # Log duty start time
            conn.execute(
                'INSERT INTO duty_logs (guard_id) VALUES (?)',
                (guard['id'],)
            )
            conn.commit()
            conn.close()
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid badge ID or password!', 'error')
            conn.close()
    
    return render_template('login.html')

def generate_unique_badge_id():
    """Generate a unique 4-digit badge ID"""
    import random
    
    conn = get_db_connection()
    
    # Get all existing badge IDs
    existing_badges = conn.execute('SELECT badge_id FROM guards').fetchall()
    existing_badge_ids = {row[0] for row in existing_badges}
    
    # Generate a unique 4-digit badge ID
    while True:
        # Generate random 4-digit number (1000-9999)
        badge_id = str(random.randint(1000, 9999))
        
        # Ensure it's not already in use
        if badge_id not in existing_badge_ids:
            conn.close()
            return badge_id

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Guard registration page"""
    if request.method == 'POST':
        full_name = request.form['full_name']
        password = request.form['password']
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        
        # Validate inputs
        if not all([full_name, password]):
            flash('Please fill in all required fields!', 'error')
            return render_template('register.html')
        
        # Auto-generate unique Badge ID
        badge_id = generate_unique_badge_id()
        
        conn = get_db_connection()
        
        # Create new guard with auto-generated Badge ID
        password_hash = generate_password_hash(password)
        try:
            conn.execute(
                'INSERT INTO guards (full_name, badge_id, password_hash, phone, email) VALUES (?, ?, ?, ?, ?)',
                (full_name, badge_id, password_hash, phone, email)
            )
            conn.commit()
            flash(f'Registration successful! Your Badge ID is: {badge_id}. Please save this for login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
            conn.close()
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard after login"""
    if 'guard_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get today's visitor count for this guard
    today = datetime.now().strftime('%Y-%m-%d')
    visitor_count = conn.execute(
        'SELECT COUNT(*) as count FROM visitor_entries WHERE guard_id = ? AND DATE(checkin_time) = ?',
        (session['guard_id'], today)
    ).fetchone()['count']
    
    # Get active visitors (checked in but not checked out)
    active_visitors = conn.execute(
        'SELECT COUNT(*) as count FROM visitor_entries WHERE guard_id = ? AND status = "checked_in"',
        (session['guard_id'],)
    ).fetchone()['count']
    
    conn.close()
    
    return render_template('dashboard.html', 
                         visitor_count=visitor_count, 
                         active_visitors=active_visitors)

@app.route('/profile')
def profile():
    """Guard profile page"""
    if 'guard_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    guard = conn.execute(
        'SELECT * FROM guards WHERE id = ?', (session['guard_id'],)
    ).fetchone()
    
    # Get duty logs for the past 7 days
    duty_logs = conn.execute('''
        SELECT login_time, logout_time, duration_minutes 
        FROM duty_logs 
        WHERE guard_id = ? 
        ORDER BY login_time DESC 
        LIMIT 10
    ''', (session['guard_id'],)).fetchall()
    
    conn.close()
    
    return render_template('profile.html', guard=guard, duty_logs=duty_logs)

@app.route('/visitor-entry', methods=['GET', 'POST'])
def visitor_entry():
    """Visitor entry form"""
    if 'guard_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        purpose_of_visit = request.form['purpose_of_visit']
        visitor_signature = request.form.get('visitor_signature', '')
        
        # Handle image upload
        visitor_image = None
        if 'visitor_image' in request.files:
            file = request.files['visitor_image']
            if file and file.filename:
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                visitor_image = filename
        
        # Save visitor entry
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO visitor_entries 
            (guard_id, visitor_name, visitor_image, purpose_of_visit, visitor_signature)
            VALUES (?, ?, ?, ?, ?)
        ''', (session['guard_id'], visitor_name, visitor_image, purpose_of_visit, visitor_signature))
        conn.commit()
        conn.close()
        
        flash('Visitor entry recorded successfully!', 'success')
        return redirect(url_for('visitor_tracking'))
    
    return render_template('visitor_entry.html')

@app.route('/visitor-tracking')
def visitor_tracking():
    """Real-time visitor tracking"""
    if 'guard_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get all visitors for today
    today = datetime.now().strftime('%Y-%m-%d')
    visitors = conn.execute('''
        SELECT * FROM visitor_entries 
        WHERE guard_id = ? AND DATE(checkin_time) = ?
        ORDER BY checkin_time DESC
    ''', (session['guard_id'], today)).fetchall()
    
    conn.close()
    
    return render_template('visitor_tracking.html', visitors=visitors)

@app.route('/checkout_visitor/<int:visitor_id>')
def checkout_visitor(visitor_id):
    """Check out a visitor"""
    if 'guard_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE visitor_entries 
        SET checkout_time = CURRENT_TIMESTAMP, status = 'checked_out'
        WHERE id = ? AND guard_id = ?
    ''', (visitor_id, session['guard_id']))
    conn.commit()
    conn.close()
    
    flash('Visitor checked out successfully!', 'success')
    return redirect(url_for('visitor_tracking'))

@app.route('/update-profile', methods=['POST'])
def update_profile():
    """Update guard profile"""
    if 'guard_id' not in session:
        return redirect(url_for('login'))
    
    full_name = request.form['full_name']
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    current_password = request.form['current_password']
    new_password = request.form.get('new_password', '')
    
    conn = get_db_connection()
    guard = conn.execute(
        'SELECT * FROM guards WHERE id = ?', (session['guard_id'],)
    ).fetchone()
    
    # Verify current password
    if not check_password_hash(guard['password_hash'], current_password):
        flash('Current password is incorrect!', 'error')
        conn.close()
        return redirect(url_for('profile'))
    
    # Update profile
    if new_password:
        password_hash = generate_password_hash(new_password)
        conn.execute('''
            UPDATE guards 
            SET full_name = ?, phone = ?, email = ?, password_hash = ?
            WHERE id = ?
        ''', (full_name, phone, email, password_hash, session['guard_id']))
    else:
        conn.execute('''
            UPDATE guards 
            SET full_name = ?, phone = ?, email = ?
            WHERE id = ?
        ''', (full_name, phone, email, session['guard_id']))
    
    conn.commit()
    conn.close()
    
    # Update session
    session['guard_name'] = full_name
    
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    """Guard logout"""
    if 'guard_id' in session:
        # Update duty log with logout time
        conn = get_db_connection()
        
        # Get the latest duty log entry for this guard
        latest_duty = conn.execute('''
            SELECT id, login_time FROM duty_logs 
            WHERE guard_id = ? AND logout_time IS NULL
            ORDER BY login_time DESC LIMIT 1
        ''', (session['guard_id'],)).fetchone()
        
        if latest_duty:
            # Calculate duration and update logout time
            logout_time = datetime.now()
            logout_time_str = logout_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Parse login time from database
            login_time_str = latest_duty['login_time']
            try:
                # Handle different possible datetime formats from database
                if 'T' in login_time_str:
                    login_time = datetime.fromisoformat(login_time_str.replace('T', ' '))
                else:
                    login_time = datetime.strptime(login_time_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # Fallback parsing
                login_time = datetime.fromisoformat(login_time_str)
            
            # Calculate duration in minutes
            duration_seconds = (logout_time - login_time).total_seconds()
            duration_minutes = max(0, int(duration_seconds / 60))  # Ensure non-negative
            
            conn.execute('''
                UPDATE duty_logs 
                SET logout_time = ?, duration_minutes = ?
                WHERE id = ?
            ''', (logout_time_str, duration_minutes, latest_duty['id']))
            conn.commit()
        
        conn.close()
        
        session.clear()
        flash('Logged out successfully!', 'success')
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
