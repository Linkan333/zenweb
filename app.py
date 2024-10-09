from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from forms import SignUpForm, SignInForm
from models import User
from __init__ import create_app, db  # Import the factory function

app = create_app()  # Use create_app to initialize the app
migrate = Migrate(app, db)  # Set up migrations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plans')
def plans():
    return render_template('plans.html')

@app.route('/account/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)

@app.route('/account/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('You have successfully signed in', 'success')
            return redirect(url_for('account'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('signin.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', username=current_user.username)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
