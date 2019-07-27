from flask import Blueprint,request,render_template
from favoriteThings.models import Favorites
main = Blueprint('main',__name__)

@main.route('/')
def home():
    page = request.args.get('page',1,type=int)
    favorites = Favorites.query.order_by(Favorites.rate.desc()).paginate(per_page=10,page=page)
    return render_template('home.html',favorites=favorites)


@main.route('/about')
def about():
    return render_template('about.html',title='about')