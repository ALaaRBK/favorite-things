
from flask import flash,url_for,redirect,request,abort,jsonify,Blueprint,render_template
from favoriteThings import db
from favoriteThings.categories.forms import CreateCategory
from favoriteThings.models import Categories,Favorites
from flask_login import current_user,login_required
from datetime import datetime
from favoriteThings.utils import addLog
categories = Blueprint('categories',__name__)

@categories.route('/createCategory',methods=['POST'])
@login_required
def createCategory():
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    newCategory = request.form.get('category')
    rate = int(float(request.form.get('rate')))
    if newCategory:
        new = Categories(name=newCategory,user_id=current_user.id,rate=rate)
        db.session.add(new)
        db.session.commit()
        log = f'Add  {newCategory} to category list  on'
        addLog(log)
        return jsonify(success=True) 
    return  jsonify(success=False)

@categories.route('/deleteCategory/<int:category_id>')
@login_required
def deleteCategory(category_id):
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    category = Categories.query.get_or_404(category_id)
    favorites = Favorites.query.filter_by(rate=category.rate).all()
    if len(favorites) != 0 :
        flash('you cant\'t Deleted','danger')
        return redirect(url_for('favorites.create'))
    if category.user_id != current_user.id:
        abort(403)
    db.session.delete(category)
    db.session.commit() 
    flash('Deleted Successfuly','success')
    log = f'Delete  {category.name} from category list  on'
    addLog(log)
    return redirect(url_for('favorites.create'))

@categories.route('/getCategories',methods=['GET'])
@login_required
def getCategories():
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    categories = Categories.query.filter_by(user_id=current_user.id).all()
    selectcategories = [];
    for category in categories:
        selectcategories.append((category.name,category.name))
    return jsonify(success=True,categories=selectcategories) 

@categories.route('/updatecategory/<int:category_id>',methods=['POST','GET'])
@login_required
def updatecategory(category_id):
    if not current_user.is_authenticated:
            return redirect(url_for('main.home'))
    categories = Categories.query.get_or_404(category_id)
    create_category=CreateCategory()
    if request.method == 'POST':
        # here we check if category is None because we can't validate in the validation method(we fill category from routes)
        if create_category.validate_on_submit() or create_category.category.data != None:
            categories.name=create_category.newCategory.data
            categories.rate=create_category.rate.data
            categories.user_id=current_user.id
            db.session.commit()
            next_page = request.args.get('next')
            log = f'Update {create_category.newCategory.data} from category list on'
            addLog(log)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        return render_template('createCategory.html',title='Create',categoryForm=create_category)            
    else:
        create_category.newCategory.data = categories.name
        create_category.rate.data = categories.rate
        log = f'Open {create_category.newCategory.data} to Update it on'
        addLog(log)
        return render_template('createCategory.html',title='Update',categoryForm=create_category)
