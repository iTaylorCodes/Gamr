from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import exc
from forms import UserAddForm
from handlers import handle_signup_errors
from models import connect_db, db, User

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

            return redirect('/signup/favorites')
        # If db errors, redirect back to try again
        except exc.SQLAlchemyError as e:
            print(f'ERROR TYPE: {type(e)}')
            flash('Something went wrong. Please try again.', 'danger')
            return redirect('/signup')
    else:
        return render_template('users/signup.html', form=form)
