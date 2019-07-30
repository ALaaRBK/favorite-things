from flask import render_template,flash,url_for,redirect,request,abort,Blueprint
from favoriteThings import db
from favoriteThings.favorites.forms import Create
from favoriteThings.categories.forms import CreateCategory
from favoriteThings.models import Favorites,Categories
from flask_login import current_user,login_required
from favoriteThings.utils import addLog
from datetime import datetime
favorites = Blueprint('favorites',__name__)

@favorites.route('/create',methods=['POST','GET'])
@login_required
def create():
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    form = Create()
    create_category=CreateCategory()
    # this section of getting categories to list them in categories choices  
    categories =Categories.query.filter_by(user_id=current_user.id).all()
    categoriesList = []
    for category in categories:
        categoriesList.append((category.name,category.name))
    form.category.choices = categoriesList
    if form.validate_on_submit():
        requestForm = request.form
        metaData = {}
        for data in requestForm:
            if '-meta-' in data:
                typeAndName = data.split("-meta-") #to get type and name of fileds from request
                metaData[typeAndName[0]] = {typeAndName[1] : request.form[data]}#store type filed, key and value we store type for viewing in front end 
        category = Categories.query.filter_by(name=form.category.data).first()
        favoriteThing = Favorites(title=form.title.data,description=form.description.data,meta_data=metaData,user_id=current_user.id,createdAt=datetime.utcnow(),group=category)
        db.session.add(favoriteThing)
        db.session.commit()
        next_page = request.args.get('next')
        log = f'Add {favoriteThing.title} to favorite list on!'
        addLog(log)
        return redirect(next_page) if next_page else redirect(url_for('favorites.create'))
    form.category.choices = categoriesList
    log = 'open create form on'
    addLog(log)
    return render_template('create.html',title='Create',form=form,categoryForm=create_category,categories=categories)

@favorites.route('/delete/<int:thing_id>',methods=['POST'])
@login_required
def deleteFavoriteThing(thing_id):
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    favoriteThing = Favorites.query.get_or_404(thing_id)
    if favoriteThing.user_id != current_user.id:
        abort(403)
    db.session.delete(favoriteThing)
    db.session.commit() 
    flash('Deleted Successfuly','success')
    log = f'Deleted {favoriteThing.title} from favorite list on'
    addLog(log)
    return redirect(url_for('main.home'))


@favorites.route('/update/<int:thing_id>',methods=['POST','GET'])
@login_required
def updateFavoriteThing(thing_id):
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    favoriteThing = Favorites.query.get_or_404(thing_id)
    # this section of getting categories to list them in the popup  
    categories = Categories.query.filter_by(user_id=current_user.id).all()
    categoriesList = []
    for category in categories:
        categoriesList.append((category.name,category.name))
    form = Create()
    create_category=CreateCategory()
    requestForm = request.form
    metaData = {}
    for data in requestForm:
        if '-meta-' in data:
            typeAndName = data.split("-meta-") #to get type and name of fileds from request
            metaData[typeAndName[0]] = {typeAndName[1] : request.form[data]}#store type filed, key and value we store type for viewing in front end 
    if request.method == 'POST':
        form.category.choices = categoriesList
        if form.validate_on_submit():
            category = Categories.query.filter_by(name=form.category.data).first()
            favoriteThing.title=form.title.data
            favoriteThing.description=form.description.data
            favoriteThing.meta_data=metaData
            favoriteThing.user_id=current_user.id
            favoriteThing.updateAt=datetime.utcnow()
            favoriteThing.category=category.id
            db.session.commit()
            next_page = request.args.get('next')
            log = f'Update {form.title.data} from favorite list on'
            addLog(log)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        return render_template('create.html',title='Create',form=form,categoryForm=create_category,categories=categories)            
    else:
        form.title.data = favoriteThing.title
        form.description.data = favoriteThing.description
        form.category.choices = categoriesList
        form.category.data = favoriteThing.group.name
        metadata = favoriteThing.meta_data
        log = f'Open {form.title.data} to Update it on'
        addLog(log)
        return render_template('create.html',title='Update',form=form,favoriteThing=favoriteThing,categoryForm=create_category,categories=categories,metadata=metadata)

