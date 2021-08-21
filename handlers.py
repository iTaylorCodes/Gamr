from flask import flash
from models import User

def handle_signup_errors(username, email, user_id):
    """Handles errors for signup or updating profile"""
    
    existing_username = User.query.filter_by(username=username).one_or_none()
    existing_email = User.query.filter_by(email=email).one_or_none()

    if existing_username and existing_username.id != user_id:
        flash("Username already taken, please try a different username.", 'danger')
        return True
    if existing_email and existing_email.id != user_id:
        flash("Account already exists with that email address.", 'danger')
        return True

    else:
        return False