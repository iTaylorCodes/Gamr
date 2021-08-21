"""Favorites model tests."""

from unittest import TestCase
from models import db, User, Favorites, Match
from run import app


class FavoritesModelTestCase(TestCase):

    """Test Favorites class."""

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

    def test_favorites_model(self):
        """Does the basic model work?"""
        
        f = Favorites(
            role='test_role',
            system='test_system',
            game1='test_game1',
            game2='test_game2',
            game3='test_game3',
            user_id=1
        )

        db.session.add(f)
        db.session.commit()

        self.assertEqual(f.role, 'test_role')
        self.assertEqual(f.system, 'test_system')
        self.assertEqual(f.game1, 'test_game1')
        self.assertEqual(f.game2, 'test_game2')
        self.assertEqual(f.game3, 'test_game3')
        self.assertEqual(f.user_id, 1)
