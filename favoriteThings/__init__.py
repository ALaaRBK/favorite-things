from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['SECRET_KEY']= 'c1a76c58367bdeaf12f088c272d0daf7'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'

db=SQLAlchemy(app)

from favoriteThings import routes