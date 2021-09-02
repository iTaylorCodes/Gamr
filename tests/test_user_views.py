from unittest import TestCase
from flask.helpers import get_flashed_messages
from flask import session
from models import AcceptedMatches, db, User, Favorites, Match
from run import app, CURR_USER_KEY

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
        self.u4 = User.signup('testuser4', 'test4@test.com', 'HASHED_PASSWORD4', 'Test4firstname', 'Test4lastname', None)
        self.uid4 = 12
        self.u4.id = self.uid4

        db.session.commit()        

        # Setup test favorites for testuser2
        self.f2 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f2id = 1
        self.f2.id = self.f2id
        self.f2.user_id = 11

        self.u2.favorites_id = 1

        db.session.add(self.f2)
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

    def test_user_login(self):
        """Does the login page display correctly? Does the view properly log in a user with the correct credentials?"""

        with self.client as c:
            # Check that the view is displaying proper HTML
            resp = c.get('/login')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Welcome back.</h2>', str(resp.data))

            # Check that the view rejects the wrong credentials
            resp = c.post('/login', data={"username": "wrong_username", "password": 'HASHED_PASSWORD1'})
            self.assertEqual(get_flashed_messages()[0], "Invalid credentials.")
            
            resp = c.post('/login', data={"username": "testuser1", "password": 'wrong_password'})
            self.assertEqual(get_flashed_messages()[0], "Invalid credentials.")

            # Check that the view redirects to set up user favorites upon first log in
            resp = c.post('/login', data={"username": "testuser1", "password": 'HASHED_PASSWORD1'})

            self.assertEqual(get_flashed_messages()[0], "Welcome, Test1firstname! Please enter some of your gaming preferences so others can match with you better. 😊")
            self.assertEqual(resp.status_code, 302)
            self.assertIn(CURR_USER_KEY, session)

            # Check that the view can log in a user who already set their favorites
            resp = c.post('/login', data={"username": "testuser2", "password": 'HASHED_PASSWORD2'})

            self.assertEqual(get_flashed_messages()[1], "Welcome Back, Test2firstname!")
            self.assertEqual(resp.status_code, 302)
            self.assertIn(CURR_USER_KEY, session)

    def test_user_logout(self):
        """Does the logout view properly log out current user and redirect?"""

        with self.client as c:
            # Check that logout view logs out current user
            resp = c.get('/logout')

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn(CURR_USER_KEY, session)
            self.assertEqual(get_flashed_messages()[0], "You have been logged out")

    def test_user_profile(self):
        """Does the show_user_profile view display the user's profile?"""

        with self.client as c:
            # Check that view displays proper HTML depending on the user
            resp = c.get(f'/users/{self.uid1}')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="card-title">testuser1</h2>', str(resp.data))

            resp = c.get(f'/users/{self.uid2}')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="card-title">testuser2</h2>', str(resp.data))

    def test_show_edit_form(self):
        """Can a non logged in user see the page? Does the view properly display the EditUserForm when user is logged in?"""
        
        with self.client as c:
            resp = c.get(f"/users/{self.uid1}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid2
                
            # Check that the view displays the correct HTML when logged in
            resp = c.get(f'/users/{self.uid2}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4>Account Info</h4>', html)

    def test_edit_user_profile(self):
        """Does the view update the user's profile?"""

        with self.client as c:
            resp = c.post(f"/users/{self.uid1}/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid1

            # Check for error handling if username already in db
            resp = c.post(f'/users/{self.uid1}/edit', data={"username": "testuser2", "email": 'test1@test.com', "password": 'HASHED_PASSWORD1', "role": 'DPS', "system": 'Playstation', "game1": 'Fallout'})

            self.assertEqual(get_flashed_messages()[0], "Username already taken, please try a different username.")
            self.assertEqual(resp.status_code, 302)

            # Check for error handling if email already in db
            resp = c.post(f'/users/{self.uid1}/edit', data={"username": "testuser1", "email": 'test2@test.com', "password": 'HASHED_PASSWORD1', "role": 'DPS', "system": 'Playstation', "game1": 'Fallout'})

            self.assertEqual(get_flashed_messages()[1], "Account already exists with that email address.")
            self.assertEqual(resp.status_code, 302)

            # Check that the view updates user data and can setup user favorites
            resp = c.post(f'/users/{self.uid1}/edit', data={"username": "testuser1", "password": 'HASHED_PASSWORD1', "first_name": "NEW_FIRST_NAME", "role": 'DPS', "system": 'Playstation', "game1": 'Fallout'})

            new_name_user = User.query.filter_by(username='testuser1').one_or_none()
            self.assertEqual(new_name_user.first_name, "NEW_FIRST_NAME")
            self.assertEqual(resp.status_code, 302)

            # Check that view rejects changes if password incorrect
            resp = c.post(f'/users/{self.uid1}/edit', data={"username": "testuser1", "password": 'wrong_password', "last_name": "NEW_LAST_NAME", "role": 'DPS', "system": 'Playstation', "game1": 'Fallout'})
            
            new_name_user = User.query.filter_by(username='testuser1').one_or_none()
            self.assertNotEqual(new_name_user.last_name, "NEW_LAST_NAME")
            self.assertEqual(get_flashed_messages()[2], "Wrong password!")
            self.assertEqual(resp.status_code, 302)

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid2

            # Check that the view updates user data and user favorites
            resp = c.post(f'/users/{self.uid2}/edit', data={"username": "testuser2", "email": 'test2@test.com', "password": 'HASHED_PASSWORD2', "first_name": "NEW_FIRST_NAME", "role": 'DPS', "system": 'XBox', "game1": 'Halo'})

            updated_user = User.query.filter_by(username='testuser2').one_or_none()
            updated_favorites = Favorites.query.filter_by(user_id=self.uid2).one_or_none()
            self.assertEqual(updated_user.first_name, "NEW_FIRST_NAME")
            self.assertEqual(updated_favorites.game1, "Halo")
            self.assertEqual(resp.status_code, 302)

    def test_delete_user(self):
        """Can a user delete their account?"""

        with self.client as c:
            resp = c.post("/users/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)
        
        with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid1

        # Check that the user is deleted from db
        resp = c.post("/users/delete")

        user_test = User.query.filter_by(id=10).one_or_none()
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(user_test)
    
    def test_show_favorites_form(self):
        """Can user see the page if they don't have favorites yet?"""
        
        with self.client as c:
            # Check that a user who already has favorites is redirected
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid2

            resp = c.get("/favorites")
            self.assertEqual(resp.status_code, 302)

            # Check that a first time user can see the form
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid1
                
            resp = c.get('/favorites')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Choose Your Favorites</h2>', html)

    def test_set_user_favorites(self):
        """Can a first time user add their favorites?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid1

            resp = c.post('/favorites', data={"role": "Healer", "system": "PC", "game1": "Diablo"})

            user_favorites = Favorites.query.filter_by(user_id=self.uid1).one_or_none()
            self.assertEqual(user_favorites.role, "Healer")
            self.assertEqual(get_flashed_messages()[0], "Your favorites have been saved! Edit them at anytime from your profile.")
            self.assertEqual(resp.status_code, 302)
    
    def test_show_homepage(self):
        """Does the anonymous homepage display? Does the match making homepage display for a logged in user?"""

        # Setup test favorites for testuser1
        self.f1 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f1id = 2
        self.f1.id = self.f1id
        self.f1.user_id = 10

        self.u1.favorites_id = 2

        db.session.add(self.f1)
        db.session.commit()
        
        with self.client as c:
            # Check that the view displays proper HTML
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h4>New to Gamr?</h4>', str(resp.data))

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid2

            # Check that the homepage displays another user's profile or redirects back if the logged in user is pulled for random user
            resp = c.get('/', follow_redirects=False)

            self.assertTrue(resp.status_code == 200 or resp.status_code == 302)

    def test_match_users(self):
        """Can a user match with another user?"""

        # Setup test favorites for testuser1
        self.f1 = Favorites(role='DPS', system='Playstation', game1='Fallout')
        self.f1id = 2
        self.f1.id = self.f1id
        self.f1.user_id = 10

        self.u1.favorites_id = 2

        db.session.add(self.f1)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid2
            # Check if a user can accept a match with another user

            resp = c.post('/10')

            self.assertEqual(resp.status_code, 302)

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid1

            # Setup test favorites for testuser4
            self.f4 = Favorites(role='DPS', system='Playstation', game1='Fallout')
            self.f4id = 4
            self.f4.id = self.f4id
            self.f4.user_id = 12

            self.u4.favorites_id = 4

            db.session.add(self.f4)
            db.session.commit()
            
            resp = c.post('11')

            accepted_match = AcceptedMatches.query.filter(AcceptedMatches.user1_id == 10, AcceptedMatches.user2_id == 11)
            self.assertTrue(accepted_match)
            self.assertEqual(resp.status_code, 302)
            


