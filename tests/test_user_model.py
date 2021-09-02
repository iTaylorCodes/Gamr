"""User model tests."""

from unittest import TestCase
from models import db, User, Favorites, Match
from run import app


class UserModelTestCase(TestCase):

    """Test User class."""

    def setUp(self):
        """Create test client and add sample data."""
        
        self.client = app.test_client()

        db.create_all()

        User.query.delete()
        Favorites.query.delete()
        Match.query.delete()

        u1 = User.signup('testuser1', 'test1@test.com', 'HASHED_PASSWORD1', 'Test1firstname', 'Test1lastname', None)
        uid1 = 1
        u1.id = uid1
        u2 = User.signup('testuser2', 'test2@test.com', 'HASHED_PASSWORD2', 'Test2firstname', 'Test2lastname', None)
        uid2 = 2
        u2.id = uid2

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does the user model work?"""

        u = User(username='testuser3', email='test3@test.com', password='NOT_HASHED_PASSWORD3', first_name='Test3firstname', last_name='Test3lastname', image_url=None)

        u.id = 3

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.username, 'testuser3')
        self.assertEqual(u.email, 'test3@test.com')
        self.assertEqual(u.first_name, 'Test3firstname')

    def test_user_repr(self):
        """Does the repr display what is expected?"""

        self.assertEqual(repr(self.u1), "<User #1: testuser1, test1@test.com>")

    def test_all_matches(self):
        """Does user.all_matches return with a list of matches?"""

        self.u1.accepts_match(self.uid2)
        self.u2.accepts_match(self.uid1)

        matches = self.u1.all_matches()

        self.assertTrue(len(matches) == 0)
        self.assertEqual(len(self.u1.matches), 1)

    def test_user_accepts_match(self):
        """Does the user.accepts_match add the other user to user.matches?
        Does the user.accepts_match set the users choice to True?"""

        match = self.u1.accepts_match(self.uid2)

        self.assertEqual(len(self.u1.matches), 1)
        self.assertEqual(self.u1.matches[0], self.u2)
        self.assertTrue(match.user1_accepted == True)
        self.assertTrue(match.user2_accepted == None)

    def test_user_signup(self):
        """Does User.signup successfully create a new user given valid credentials?
        Does User.signup fail to create a new user if any of the validations fail?"""

        new_user = User.signup(username='testuser4', email='test4@test.com', password='HASHED_PASSWORD4', first_name='Test4firstname', last_name='Test4lastname', image_url=None)

        new_user.id = 4
        db.session.commit()
        new_user_test = User.query.get(new_user.id)
        self.assertEqual(new_user_test.username, 'testuser4')
        self.assertEqual(new_user_test.email, 'test4@test.com')

        # Is the password a bcrypt hash string?
        self.assertTrue(new_user_test.password.index('$2b$') != -1)

    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?
        Does User.authenticate fail to return a user when the username is invalid?
        Does User.authenticate fail to return a user when the password is invalid?"""

        self.assertTrue(User.authenticate('testuser1', 'HASHED_PASSWORD1'))
        self.assertFalse(User.authenticate('not_testuser1', 'HASHED_PASSWORD1'))
        self.assertFalse(User.authenticate('testuser1', 'wrong_password'))