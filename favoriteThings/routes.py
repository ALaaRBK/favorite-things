from flask import render_template,Flask,url_for,redirect,flash,request,jsonify
from favoriteThings import app,bcrypt,db
from favoriteThings.models import User,Favorites,Categories
from favoriteThings.forms import RegistrationForm,LoginForm,Create,CreateCategory
from flask_login import login_user,current_user,logout_user,login_required
from datetime import datetime


@app.route('/')
@login_required
def home():
    favorites = Favorites.query.order_by(Favorites.rate.desc())
    return render_template('home.html',favorites=favorites)


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

@app.route('/create',methods=['POST','GET'])
@login_required
def create():
    if not current_user.is_authenticated:
            return redirect(url_for('home'))
    form = Create()
    create_category=CreateCategory()
    categories =Categories.query.filter_by(user_id=current_user.id).all()
    categoriesList = []
    for category in categories:
        categoriesList.append((category.name,category.name))
    if form.validate_on_submit() or (form.category.data is not None and request.method == 'POST'):
        category = Categories.query.filter_by(name=form.category.data).first()
        if form.description.data and len(form.description.data) < 10:
            form.description.errors.append('Description Field must be minimum 10 and 20 characters long')
            return render_template('create.html',title='Create',form=form,categoryForm=CreateCategory,categories=categories)
        favoriteThing = Favorites(title=form.title.data,description=form.description.data,meta_data=form.metadata.data,user_id=current_user.id,createdAt=datetime.utcnow(),group=category)
        db.session.add(favoriteThing)
        db.session.commit()
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form.category.choices = categoriesList
    return render_template('create.html',title='Create',form=form,categoryForm=create_category,categories=categories)


@app.route('/createCategory',methods=['POST'])
@login_required
def createCategory():
    if not current_user.is_authenticated:
            return redirect(url_for('home'))
    newCategory = request.form.get('category')
    rate = int(float(request.form.get('rate')))
    if newCategory:
        new = Categories(name=newCategory,user_id=current_user.id,rate=rate)
        db.session.add(new)
        db.session.commit()
        return jsonify(success=True) 
    return  jsonify(success=False)
