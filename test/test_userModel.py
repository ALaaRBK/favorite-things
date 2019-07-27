import unittest
from favoriteThings import create_app, db
from favoriteThings.models import User
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

class UserModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_password = 'testing'

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.bcrypt = Bcrypt(self.app)
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_username_value(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        username = 'test'
        u = User(username=username,email='test@test.com',password=pw)
        db.session.add(u)
        db.session.commit()
        remove_user(username)
        self.assertTrue(u.username == username)


    def test_username_value_null(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        username = None
        u = User(username=username,email='test@test.com',password=pw)
        with self.assertRaises(IntegrityError):
            db.session.add(u)
            db.session.commit()
            remove_user('test')

    def test_email_value(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        email = 'test@test.com'
        u = User(username='test',email= email,password=pw)
        db.session.add(u)
        db.session.commit()
        remove_user('test')
        self.assertTrue(u.email == email)


    def test_email_value_null(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        email = None
        u = User(username='test',email= email,password= pw)
        with self.assertRaises(IntegrityError):
            db.session.add(u)
            db.session.commit()
            remove_user('test')

    def test_password_hash_check(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u = User(username='test',email='test@test.com',password=pw)
        db.session.add(u)
        db.session.commit()
        q_u = User.query.filter_by(username='test').first()
        remove_user('test')
        self.assertTrue(self.bcrypt.check_password_hash(q_u.password, self.test_password))


    def test_id_not_repeated(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u1 = User(username='test', email='test@test.com', password=pw)
        u2 = User(username='test2',email= 'test2@test.com',password=pw)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        q_u1 = User.query.get(u1.id)
        q_u2 = User.query.get(u2.id)
        remove_user('test')
        remove_user('test2')
        self.assertFalse(q_u1.id == q_u2.id)



    def test_username_must_be_unique(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u1 = User(username='test',email='test@test.com', password=pw)
        u2 = User(username='test',email='test2@test.com',password= pw)
        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(IntegrityError):
            db.session.commit()
            remove_user('test')

    def test_email_must_be_unique(self):
        pw = self.bcrypt.generate_password_hash(self.test_password).decode('utf-8')
        u1 = User(username='test',email='test@test.com',password=pw)
        u2 = User(username='test2', email='test@test.com',password=pw)
        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(IntegrityError):
            db.session.commit()
            remove_user('test')
            remove_user('test2')

def remove_user(username):
    user=User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()


if __name__ == '__main__':
    unittest.main()



