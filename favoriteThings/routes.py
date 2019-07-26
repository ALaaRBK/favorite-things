from flask import render_template,Flask,url_for,redirect,flash
from favoriteThings import app
from favoriteThings.models import User,Favorites
from favoriteThings.forms import RegistrationForm,LoginForm



@app.route('/')
def home():
    return render_template('index.html',title='Favorite Things')

@app.route('/about')
def about():
    return render_template('about.html',title='about')


@app.route('/register',methods=['POST','GET'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)
    

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            flash('Login Successful','success')        
            return redirect(next_page) if next_page else redirect(url_for('home'))
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


