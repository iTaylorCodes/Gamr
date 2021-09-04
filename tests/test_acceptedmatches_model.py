"""AcceptedMatches model tests."""

from unittest import TestCase
from models import db, User, Favorites, Match, AcceptedMatches
from app import app


class AcceptedMatchesModelTestCase(TestCase):

    """Test AcceptedMatches class."""

    def setUp(self):
        """Create test client and add sample data."""

        self.client = app.test_client()
        
        db.create_all()

        User.query.delete()
        Favorites.query.delete()
        Match.query.delete()

        self.u1 = User.signup('testuser1', 'test1@test.com', 'HASHED_PASSWORD1', 'Test1firstname', 'Test1lastname', None)
        self.uid1 = 1
        self.u1.id = self.uid1
        self.u2 = User.signup('testuser2', 'test2@test.com', 'HASHED_PASSWORD2', 'Test2firstname', 'Test2lastname', None)
        self.uid2 = 2
        self.u2.id = self.uid2

        db.session.commit()

    def tearDown(self):
        """Runs after every test."""

        db.session.rollback()
        return super().tearDown()

    def test_match_model(self):
        """Does the basic model work?"""

        m = AcceptedMatches(
            user1_id=self.uid1,
            user2_id=self.uid2
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(m.user1_id, 1)
        self.assertEqual(m.user2_id, 2)


