from flask import Flask, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import exc
from forms import UserAddForm, UserLoginForm
from handlers import handle_signup_errors
from models import connect_db, db, User, Favorites

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object('config.ProductionConfig')
elif app.config["ENV"] == "testing":
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')
    
toolbar = DebugToolbarExtension(app)

connect_db(app)

########################################################
# User Signup/Login/Logout Routes:

@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup"""

    form = UserAddForm()

    if form.validate_on_submit():
        # Attempt to create a user

        errors = handle_signup_errors(form.username.data, form.email.data, None)
        if errors:
            return render_template('users/signup.html', form=form)

        try:
            User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()

            return redirect('/login')
        # If db errors, redirect back to try again
        except exc.SQLAlchemyError as e:
            print(f'ERROR TYPE: {type(e)}')
            flash('Something went wrong. Please try again.', 'danger')
            return redirect('/signup')
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.first_name}!", "success")
            return redirect('/')
        
        flash("Invalid credentials.", "danger")

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user"""

    do_logout()
    flash("You have been logged out", "success")
    return redirect('/login')

########################################################
# General User Routes:

@app.route('/users/<int:user_id>')
def show_user_profile(user_id):
    """Show user's profile"""

    user = User.query.get_or_404(user_id)
    favorites = Favorites.query.filter_by(user_id=user.id).one_or_none()

    return render_template('users/detail.html', user=user, favorites=favorites)

########################################################
# Homepage:

@app.route('/')
def show_homepage():
    """Show homepage"""

    return render_template('home.html')