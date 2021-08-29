from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    image_url = StringField('(Optional) Profile Picture')

class UserLoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserFavoritesForm(FlaskForm):
    """Form for adding user's favorites."""

    role = SelectField('Favorite Role', choices=['DPS', 'Healer', 'Support', 'Tank'], validators=[DataRequired()])
    system = SelectField('Favorite System', choices=['Nintendo Switch', 'PC', 'Playstation', 'VR', 'Xbox'], validators=[DataRequired()])
    game1 = SelectField('Favorite Game 1', choices=[], validators=[DataRequired()], validate_choice=False)
    game2 = SelectField('Favorite Game 2', choices=[], validate_choice=False)
    game3 = SelectField('Favorite Game 3', choices=[], validate_choice=False)

class EditUserForm(FlaskForm):
    """Form for editing a user's profile."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    bio = StringField('Bio')
    discord_username = StringField('Discord Username')
    image_url = StringField('Profile Picture')
    role = SelectField('Favorite Role', choices=['DPS', 'Healer', 'Support', 'Tank'], validators=[DataRequired()])
    system = SelectField('Favorite System', choices=['Nintendo Switch', 'PC', 'Playstation', 'VR', 'Xbox'], validators=[DataRequired()])
    game1 = SelectField('Favorite Game', choices=[], validators=[DataRequired()], validate_choice=False)
    game2 = SelectField('2nd Favorite Game', choices=[], validate_choice=False)
    game3 = SelectField('3rd Favorite Game', choices=[], validate_choice=False)
    password = PasswordField('Password', validators=[Length(min=6)])
