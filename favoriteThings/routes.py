from flask import render_template,Flask,url_for,redirect,flash,request
from favoriteThings import app,bcrypt,db
from favoriteThings.models import User,Favorites
from favoriteThings.forms import RegistrationForm,LoginForm
from flask_login import login_user,current_user,logout_user,login_required

@app.route('/')
@login_required
def home():
    return render_template('index.html',title='Favorite Things')

@app.route('/about')
def about():
    return render_template('about.html',title='about')


@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)
    

@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login Successful','success')        
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. please check email and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


