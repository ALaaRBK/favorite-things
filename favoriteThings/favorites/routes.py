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
        log = f'Add {favoriteThing.title} to favorite list on!'
        addLog(log)
        return redirect(next_page) if next_page else redirect(url_for('main.home'))
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
            log = f'Update {form.title.data} from favorite list on'
            addLog(log)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        return render_template('create.html',title='Create',form=form,categoryForm=create_category,categories=categories)            
    else:
        form.title.data = favoriteThing.title
        form.description.data = favoriteThing.description
        form.category.choices = categoriesList
        form.category.data = favoriteThing.group.name
        log = f'Open {form.title.data} to Update it on'
        addLog(log)
        return render_template('create.html',title='Update',form=form,favoriteThing=favoriteThing,categoryForm=create_category,categories=categories)

