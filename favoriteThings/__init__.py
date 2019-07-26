from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)



app.config['SECRET_KEY']= 'c1a76c58367bdeaf12f088c272d0daf7'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'

db=SQLAlchemy(app)
bcrypt = Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view='login'#if user not authorized to access to the page this will redirect to login page
login_manager.login_message_category='info' #to show messages when got denied access to pages

from favoriteThings import routes