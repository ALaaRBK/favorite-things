import unittest
from favoriteThings import create_app, db
from flask_wtf.csrf import generate_csrf
from favoriteThings.models import User

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.test_client = self.app.test_client()

    def tearDown(self):
        pass

    def test_register(self):
        requst = self.test_client.get('/register')
        # did the request fail?
        self.assertEqual(requst.status_code, 200)
        # did we get the expected page?
        self.assertTrue('<legend class="border-bottom mb-4">Rigister NOW</legend>' in requst.get_data(as_text=True))
        user_data = {
            'csrf_token': generate_csrf(),
            'username': 'test1',
            'email': 'test1@test1.com',
            'password': 'testing',
        }
        # try to POST a user into the database
        requst = self.test_client.post('/register', data=user_data, follow_redirects=True)
        user = User.query.filter_by(username=user_data['username']).first()
        # did the request fail?
        self.assertEqual(requst.status_code, 200)
        # did it actually create the user?
        self.assertIsNotNone(user)

    def test_login(self):
        self.test_client.get('/register')
        user_data = {
            'csrf_token': generate_csrf(),
            'username': 'test1',
            'email': 'test1@test1.com',
            'password': 'testing',
        }
        # register the user
        self.test_client.post('/register', data=user_data, follow_redirects=True)
        # request login page
        requst = self.test_client.get('/login')
        # was the request successful?
        self.assertEqual(requst.status_code, 200)
        # did we get the expected page?
        self.assertTrue('<legend class="border-bottom mb-4">Login</legend>' in requst.get_data(as_text=True))
        # login the user
        requst = self.test_client.post('/login', data=user_data, follow_redirects=True)
        # check if the user authenticated
        user = User.query.filter_by(email=user_data['email']).first()
        self.assertTrue(user.is_authenticated)

if __name__ == '__main__':
    unittest.main()