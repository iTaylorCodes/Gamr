from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('(Optional) Image URL')

class UserLoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserFavoritesForm(FlaskForm):
    """Form for adding users favorites."""

    role = StringField('Favorite Role', validators=[DataRequired()])
    system = StringField('Favorite System', validators=[DataRequired()])
    game1 = StringField('Favorite Game 1', validators=[DataRequired()])
    game2 = StringField('Favorite Game 2')
    game3 = StringField('Favorite Game 3')