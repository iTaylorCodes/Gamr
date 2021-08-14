from unittest import TestCase
from flask.helpers import get_flashed_messages
from models import db, User, Favorites, Match
from run import app

class UserViewsTestCase(TestCase):
    
    """Test views for user."""

    def setUp(self):
        """Create test client and add sample data."""

        self.client = app.test_client()

        db.create_all()

        User.query.delete()
        Favorites.query.delete()
        Match.query.delete()

        self.u1 = User.signup('testuser1', 'test1@test.com', 'HASHED_PASSWORD1', 'Test1firstname', 'Test1lastname', None)
        self.uid1 = 10
        self.u1.id = self.uid1
        self.u2 = User.signup('testuser2', 'test2@test.com', 'HASHED_PASSWORD2', 'Test2firstname', 'Test2lastname', None)
        self.uid2 = 11
        self.u2.id = self.uid2
        db.session.commit()

    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_signup_view(self):
        """Does the signup page display correctly? Does the view catch duplicate account errors? Does the view catch database errors?"""

        with self.client as c:
            # Check that view is displaying proper HTML
            resp = c.get('/signup')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Join Gamr today.</h2>', str(resp.data))

            # Check for error handling if username already in db
            resp = c.post('/signup', data={"username": "testuser1", "email": 'test@test.com', "password": 'HASHED_PASSWORD1', "first_name": 'Test1firstname', "last_name": 'Test1lastname', "image_url": None})
            
            self.assertEqual(get_flashed_messages()[0], "Username already taken, please try a different username.")
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Join Gamr today.</h2>', str(resp.data))

            # Check for error handling if email already in db
            resp = c.post('/signup', data={"username": "testuser", "email": 'test1@test.com', "password": 'HASHED_PASSWORD1', "first_name": 'Test1firstname', "last_name": 'Test1lastname', "image_url": None})

            self.assertEqual(get_flashed_messages()[0], "Account already exists with that email address.")
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Join Gamr today.</h2>', str(resp.data))

            # Check that view can add a user to db
            resp = c.post('/signup', data={"username": "testuser3", "email": 'test3@test.com', "password": 'HASHED_PASSWORD3', "first_name": 'Test3firstname', "last_name": 'Test3lastname', "image_url": None})

            new_user_test = User.query.filter_by(username='testuser3').one_or_none()
            self.assertEqual(new_user_test.username, 'testuser3')
            self.assertEqual(new_user_test.email, 'test3@test.com')
            self.assertEqual(resp.status_code, 302)
