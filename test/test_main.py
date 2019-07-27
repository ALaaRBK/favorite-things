import unittest
from flask import current_app
from favoriteThings import create_app, db

class BasicTestCased(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_app_exists(self):
        self.assertFalse(current_app is None)
        self.assertFalse(db is None)

    def test_db_exists(self):
        self.assertFalse(db is None)


if __name__ == '__main__':
    unittest.main()



