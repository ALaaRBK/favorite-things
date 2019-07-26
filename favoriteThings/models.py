from datetime import datetime
from favoriteThings import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    favorite = db.relationship('Favorites',backref='auther',lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Favorites(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(20),nullable=False)
    description=db.Column(db.String(),nullable=True)
    createdAt=db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    updateAt = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    meta_data= db.Column(db.String(),nullable=True)

    def __repr__(self):
        return f"Favorites('{self.title}','{self.createdAt}','{self.description}','{self.user_id}','{self.updateAt})"
