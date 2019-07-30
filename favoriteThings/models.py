from datetime import datetime
from favoriteThings import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    favorite = db.relationship('Favorites',backref='auther',lazy=True)
    category = db.relationship('Categories',backref='auther',lazy=True)
    log = db.relationship('AuditLog',backref='auther',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Favorites(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(20),nullable=False)
    description=db.Column(db.String(),nullable=True)
    createdAt=db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    updateAt = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    meta_data= db.Column(db.PickleType(),nullable=True)
    category = db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)


    def __repr__(self):
        return f"Favorites('{self.title}','{self.createdAt}','{self.description}','{self.user_id}','{self.updateAt},'{self.meta_data})"
class Categories(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    rate=db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    favorites = db.relationship('Favorites',backref='group',lazy=True)
    def __repr__(self):
        return f"Categories('{self.name}','{self.rate}','{self.user_id}')"

class AuditLog(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    log=db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"AuditLog('{self.log}')"