from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class Match(db.Model):

    """Users who have been matched.
    Boolean if they accepted eachother."""

    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)

    user1_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade")
    )

    user2_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade")
    )

    user1_accepted = db.Column(db.Boolean)

    user2_accepted = db.Column(db.Boolean)

class AcceptedMatches(db.Model):

    """All matches that have been accepted between users."""

    __tablename__ = 'accepted_matches'

    user1_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    )

    user2_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    )


class Favorites(db.Model):

    """User favorites"""

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)

    role = db.Column(db.Text, nullable=False)

    system = db.Column(db.Text, nullable=False)

    game1 = db.Column(db.Text)

    game2 = db.Column(db.Text)

    game3 = db.Column(db.Text)

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='cascade')
    )


class User(db.Model):

    """User in the db"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    email = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, default="/static/images/default-pic.png")

    bio = db.Column(db.Text)

    discord_username = db.Column(db.Text)

    favorites_id = db.Column(
        db.Integer, 
        db.ForeignKey('favorites.id', ondelete='cascade')
    )

    matches = db.relationship(
        "User",
        secondary="matches",
        primaryjoin=(Match.user1_id == id),
        secondaryjoin=(Match.user2_id == id)
    )

    def __repr__(self):
        """Representation of the User class."""

        return f"<User #{self.id}: {self.username}, {self.email}>"

    def all_matches(self):
        """A list of users matched with the logged in user."""

        matches_as_user1 = AcceptedMatches.query.filter(AcceptedMatches.user1_id == self.id).all()
        matches_as_user2 = AcceptedMatches.query.filter(AcceptedMatches.user2_id == self.id).all()

        all_matches = []

        for match in matches_as_user1:
            user = User.query.get_or_404(match.user2_id)
            all_matches.append(user)

        for match in matches_as_user2:
            user = User.query.get_or_404(match.user1_id)
            all_matches.append(user)

        return all_matches

    def accepts_match(self, other_user_id):
        """Accepts a match between 2 users and adds it to matches table."""

        match = Match.query.filter(self.id == Match.user1_id, other_user_id == Match.user2_id).one_or_none()
        
        if match == None:
            match = Match.query.filter(self.id == Match.user2_id, other_user_id == Match.user1_id).one_or_none()
        
        if not match:
            match = Match(
                user1_id=self.id,
                user2_id=other_user_id
            )
            db.session.add(match)
            db.session.commit()

        if match.user1_id == self.id:
            match.user1_accepted = True
            db.session.commit()
        else:
            match.user2_accepted = True
            db.session.commit()

        return match

    @classmethod
    def signup(cls, username, email, password, first_name, last_name, image_url):
        """Sign up user.

        Hashes password and adds user to db.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect this database to the application."""

    db.app = app
    db.init_app(app)