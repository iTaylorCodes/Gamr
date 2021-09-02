from unittest import TestCase
from flask.helpers import get_flashed_messages
from models import AcceptedMatches, db, User, Favorites, Match
from run import app, CURR_USER_KEY

class MatchesViewsTestCase(TestCase):
    
    """Test views for matches."""

    def setUp(self):
        """Create test client and add sample data."""

        self.client = app.test_client()

        db.create_all()

        User.query.delete()
        Favorites.query.delete()
        Match.query.delete()
        AcceptedMatches.query.delete()

        self.u1 = User.signup('testuser1', 'test1@test.com', 'HASHED_PASSWORD1', 'Test1firstname', 'Test1lastname', None)
        self.uid1 = 1
        self.u1.id = self.uid1
        self.u2 = User.signup('testuser2', 'test2@test.com', 'HASHED_PASSWORD2', 'Test2firstname', 'Test2lastname', None)
        self.uid2 = 2
        self.u2.id = self.uid2
        self.u3 = User.signup('testuser3', 'test3@test.com', 'HASHED_PASSWORD3', 'Test3firstname', 'Test3lastname', None)
        self.uid3 = 3
        self.u3.id = self.uid3
        self.u4 = User.signup('testuser4', 'test4@test.com', 'HASHED_PASSWORD4', 'Test4firstname', 'Test4lastname', None)
        self.uid4 = 4
        self.u4.id = self.uid4

        db.session.commit()

        # Setup test favorites
        self.f1 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f1id = 1
        self.f1.id = self.f1id
        self.f1.user_id = 1

        self.u1.favorites_id = 1

        self.f2 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f2id = 2
        self.f2.id = self.f2id
        self.f2.user_id = 2

        self.u2.favorites_id = 2

        self.f3 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f3id = 3
        self.f3.id = self.f3id
        self.f3.user_id = 3

        self.u3.favorites_id = 3

        self.f4 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f4id = 4
        self.f4.id = self.f4id
        self.f4.user_id = 4

        self.u3.favorites_id = 4

        db.session.add_all([self.f1, self.f2, self.f3, self.f4])
        db.session.commit()

    def tearDown(self):
        """Runs after every test"""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_show_matches(self):
        """Does the show_matches view show a list of users matched with the current user?"""

        with self.client as c:
            # Check that the user is redirected if not logged in
            resp = c.get('/matches')

            self.assertEqual(get_flashed_messages()[0], "Access unauthorized.")
            self.assertEqual(resp.status_code, 302)

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid1
            # Check that the user is redirected if they have no matches
            resp = c.get('/matches')

            self.assertEqual(get_flashed_messages()[1], "You don't have any matches yet, let's make some matches!")
            self.assertEqual(resp.status_code, 302)

            