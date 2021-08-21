from unittest import TestCase

from flask.helpers import get_flashed_messages
from models import db, User, Favorites, Match
from handlers import handle_signup_errors
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
        self.uid1 = 7
        self.u1.id = self.uid1
        self.u2 = User.signup('testuser2', 'test2@test.com', 'HASHED_PASSWORD2', 'Test2firstname', 'Test2lastname', None)
        self.uid2 = 8
        self.u2.id = self.uid2
        db.session.commit()

    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_handle_signup_errors(self):
        """Does the handle_signup_errors handler prevent users
            from signing up with an in-use username or email?
            Does it flash the error message to user?"""

        with app.test_request_context('/signup'):
            test1 = handle_signup_errors('testuser1', 'test@test.com', None)

            self.assertTrue(test1)
            self.assertEqual(get_flashed_messages()[0], "Username already taken, please try a different username.")

        with app.test_request_context('/signup'):
            test2 = handle_signup_errors('testuser', 'test1@test.com', None)

            self.assertTrue(test2)
            self.assertEqual(get_flashed_messages()[0], "Account already exists with that email address.")
