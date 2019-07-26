from flask import render_template,Flask,url_for,redirect,flash,request,jsonify
from favoriteThings import app,bcrypt,db
from favoriteThings.models import User,Favorites,Categories
from favoriteThings.forms import RegistrationForm,LoginForm,Create,CreateCategory
from flask_login import login_user,current_user,logout_user,login_required
from datetime import datetime


@app.route('/')
@login_required
def home():
    page = request.args.get('page',1,type=int)
    favorites = Favorites.query.order_by(Favorites.rate.desc()).paginate(per_page=10,page=page)
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
    # this section of getting categories to list them in the popup  
    categories =Categories.query.filter_by(user_id=current_user.id).all()
    categoriesList = []
    for category in categories:
        categoriesList.append((category.name,category.name))
    #here we check if category is None because we can't validate in the validation method(we fill category from routes) 
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

@app.route('/delete/<int:thing_id>',methods=['POST'])
@login_required
def deleteFavoriteThing(thing_id):
    if not current_user.is_authenticated:
            return redirect(url_for('home'))
    favoriteThing = Favorites.query.get_or_404(thing_id)
    if favoriteThing.user_id != current_user.id:
        abort(403)
    db.session.delete(favoriteThing)
    db.session.commit() 
    flash('Deleted Successfuly','success')
    return redirect(url_for('home'))


@app.route('/update/<int:thing_id>',methods=['POST','GET'])
@login_required
def updateFavoriteThing(thing_id):
    if not current_user.is_authenticated:
            return redirect(url_for('home'))
    favoriteThing = Favorites.query.get_or_404(thing_id)
    # this section of getting categories to list them in the popup  
    categories = Categories.query.filter_by(user_id=current_user.id).all()
    categoriesList = []
    for category in categories:
        categoriesList.append((category.name,category.name))
    form = Create()
    create_category=CreateCategory()
    if request.method == 'POST':
        # here we check if category is None because we can't validate in the validation method(we fill category from routes)
        if form.validate_on_submit() or form.category.data != None:
            category = Categories.query.filter_by(name=form.category.data).first()
            favoriteThing.title=form.title.data
            favoriteThing.description=form.description.data
            favoriteThing.meta_data=form.metadata.data
            favoriteThing.user_id=current_user.id
            favoriteThing.updateAt=datetime.utcnow()
            favoriteThing.rate=category.rate
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        return render_template('create.html',title='Create',form=form,categoryForm=create_category,categories=categories)            
    else:
        form.title.data = favoriteThing.title
        form.description.data = favoriteThing.description
        form.category.choices = categoriesList
        form.category.data = favoriteThing.group.name
        return render_template('create.html',title='Update',form=form,favoriteThing=favoriteThing,categoryForm=create_category,categories=categories)


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

@app.route('/deleteCategory/<int:category_id>')
@login_required
def deleteCategory(category_id):
    if not current_user.is_authenticated:
            return redirect(url_for('home'))
    category = Categories.query.get_or_404(category_id)
    if category.user_id != current_user.id:
        abort(403)
    db.session.delete(category)
    db.session.commit() 
    flash('Deleted Successfuly','success')
    return redirect(url_for('create'))

@app.route('/getCategories',methods=['GET'])
@login_required
def getCategories():
    if not current_user.is_authenticated:
            return redirect(url_for('home'))
    categories = Categories.query.filter_by(user_id=current_user.id).all()
    selectcategories = [];
    for category in categories:
        selectcategories.append((category.name,category.name))
    return jsonify(success=True,categories=selectcategories) 
    