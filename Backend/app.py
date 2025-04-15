import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)

# DB 연결 설정 (MySQL + SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://for_flask:25FlaskOnly25@@localhost/habit_tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    if 'user_id' in session:
        return f"Welcome to the Habit Tracker, User ID: {session['user_id']}!"
    else:
        return redirect(url_for('auth', mode='login'))

@app.route('/auth/<mode>', methods=['GET', 'POST'])
def auth(mode):
    if mode not in ['login', 'signup']:
        return redirect(url_for('auth', mode='login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if mode == 'signup':
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'danger')
                return redirect(url_for('auth', mode='signup'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('auth', mode='login'))

        elif mode == 'login':
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!', 'danger')
                return redirect(url_for('auth', mode='login'))

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth', mode='login'))

# ✅ 여기서 테이블 생성하도록 변경
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
