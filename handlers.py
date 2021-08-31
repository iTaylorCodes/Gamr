from flask import flash
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
import os
import requests
from models import User, db

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
    
def handle_game_choices():
    """Use the IGDB API to give the user choices for their favorite video games"""

    client_id = os.environ.get("IGDB_CLIENT_ID")
    client_secret = os.environ.get("IGDB_CLIENT_SECRET")
    auth_resp = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
    
    auth_resp_dict = auth_resp.json()
    auth_token = auth_resp_dict['access_token']

    headers = {
        'Accept': 'application/json',
        'Client-ID': f'{client_id}',
        'Authorization': f'Bearer {auth_token}'
        }
    resp = requests.post('https://api.igdb.com/v4/games', headers=headers, data='fields name; where release_dates.platform = (130,48,49,6) & themes != (42); limit 500;')

    resp_dict = resp.json()

    games = []

    for key in resp_dict:
        games.append(key['name'])
    
    return games

def random_user():
    return User.query.options(load_only('id')).offset(
            func.floor(
                func.random() *
                db.session.query(func.count(User.id))
            )
        ).limit(1).all()