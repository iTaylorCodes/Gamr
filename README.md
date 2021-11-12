<p align="center">
  <a href="https://app-gamr.herokuapp.com/">
    <img alt="Gamr" src="static/images/gamrFullLogo.png" width="250" />
  </a>
</p>

[![Build Status](https://app.travis-ci.com/iTaylorCodes/Gamr.svg?branch=main)](https://app.travis-ci.com/iTaylorCodes/Gamr)
[![Coverage Status](https://coveralls.io/repos/github/iTaylorCodes/Capstone-1/badge.svg?branch=main)](https://coveralls.io/github/iTaylorCodes/Capstone-1?branch=main)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/be59e436ae6b4e4cbdfa9d07ca8f617c)](https://www.codacy.com/gh/iTaylorCodes/Capstone-1/dashboard?utm_source=github.com&utm_medium=referral&utm_content=iTaylorCodes/Capstone-1&utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/0e76ad1c18a27f0e2a4f/maintainability)](https://codeclimate.com/github/iTaylorCodes/Capstone-1/maintainability)

Gamr is an application that makes it easier for video game players, gamers, to find other gamers to play with by matching them together based on their game preferences and favorite role to play as.

# Local Setup

If you'd like to setup a local version of Gamr, follow these steps:

## 1. Clone the repository

`$ git clone https://github.com/iTaylorCodes/Capstone-1.git`

`$ cd capstone-1`

## 2. Install all requirements

`$ pip install requirements.txt`

## 3. Create a local PostgreSQL db and setup tables

`$ createdb gamr`

`$ python seed.py`

## 4. Setup IGDB API

Visit IGDB.com and signup to receive the required Client-ID and Client-Secret environment variables.

## 5. Run the flask server and navigate your browser to http://localhost:5000/

`$ flask run`

# API

Gamr uses the IGDB API to receive a list of games that a user may select for their top 3 to add to their profiles.

# Testing

To fully test the application, running

`$ python -m unittest discover tests`

will test all routes, models, and handler functions.

# Routes and User Flow

The first route users will visit is `/` where users who are not logged in will see the Gamr Homepage with a link to signup.

Users are then sent to the `/signup` route where they can create an account.

They will then visit the `/login` route to verify their credentials.

Upon first login they will be redirected to the `/favorites` route where they will have to setup their video game preferences to be better matched with other users.

Once they have their favorites set up, the user will be redirected back to `/` where they will see other users profiles with a choice to Match or Skip.

From the navbar users can visit their own profile page at `/users/<user_id>` and from there they may visit `/users/<user_id>/edit` to edit their account info or favorites, or `/users/delete` to delete their account.

If the user has made matches with other users they may also visit `/matches`, from their profile or the navbar, to view a list of their matches and from there, `/matches/<matched_users_id>/delete` to delete a match with another user.

And finally a user may visit `/logout` to logout.

# Deployment

Gamr is currently deployed using Heroku.
You can visit it at: https://app-gamr.herokuapp.com/

# Technologies Used

Gamr was created using:

- Python3
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-WTF
- Jinja
- HTML
- CSS
