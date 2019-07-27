import unittest
from datetime import datetime
from favoriteThings import create_app, db
from favoriteThings.models import User,Favorites,Categories
from flask_bcrypt import Bcrypt

class FavoritestModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bcrypt = Bcrypt(self.app)
        self.test_user = User(username='test9',email= 'test10@test.com',
                              password=self.bcrypt.generate_password_hash('testing123_$%').decode('utf-8'))
        db.session.add(self.test_user)
        db.session.commit()
        self.test_categories = Categories(name="bood",rate= 1,user_id= self.test_user.id)
        db.session.add(self.test_categories)
        db.session.commit()
        self.test_favorites = Favorites(title='Burger',rate= self.test_categories.rate,user_id= self.test_user.id,
                            createdAt=datetime.utcnow(),
                            updateAt=datetime.utcnow())
        db.session.add(self.test_favorites)
        db.session.commit()

    def tearDown(self):
        # pass
        user = User.query.get(self.test_user.id)
        category= Categories.query.get(self.test_categories.id)
        favorite = Favorites.query.get(self.test_favorites.id)
        db.session.delete(favorite)
        db.session.commit()
        db.session.delete(category)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        db.session.remove()
        self.app_context.pop()

    def test_request_values(self):
        favorite = Favorites(title='Burger',
                            description='Burger with every adds',
                            rate= self.test_categories.rate,
                            user_id= self.test_user.id,
                            meta_data='Burger with every adds',
                            createdAt=datetime.utcnow(),
                            updateAt=datetime.utcnow())

  
        db.session.add(favorite)
        db.session.commit()
        get_favorite = Favorites.query.get(favorite.id)
        self.assertEqual(get_favorite.title, favorite.title)
        self.assertEqual(get_favorite.description, favorite.description)
        self.assertEqual(get_favorite.createdAt, favorite.createdAt)
        self.assertEqual(get_favorite.createdAt, favorite.createdAt)
        self.assertEqual(get_favorite.meta_data, favorite.meta_data)
        self.assertEqual(get_favorite.rate, favorite.rate)
        self.assertEqual(get_favorite.user_id, favorite.user_id)
        db.session.delete(get_favorite)
        db.session.commit()



if __name__ == '__main__':
    unittest.main()

