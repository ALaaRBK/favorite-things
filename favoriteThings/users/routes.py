
from flask import render_template,flash,url_for,redirect,request,Blueprint
from favoriteThings import db,bcrypt
from favoriteThings.users.forms import RegistrationForm,LoginForm
from favoriteThings.models import User
from flask_login import login_user,current_user,logout_user
from datetime import datetime
from favoriteThings.utils import addLog
users = Blueprint('users',__name__)

@users.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('main.home'))
    return render_template('register.html',title='Register',form=form)
    

@users.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login Successful','success')
            log = 'Logged in on!'
            addLog(log)       
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login Unsuccessful. please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))