# Routes

## Homepage:

`/`

Shows the homepage.
If logged in:
Shows another user's profile card with Match Us or Skip buttons
Else:
Returns a homepage template that describes Gamr with a link to signup.

---

## Signup/Login/Logout Routes:

`/signup`

A form to create a new account, redirects to `/login`

`/login`

A form to login, first time users redirect to `/favorites` else redirects to `/`

`/logout`

Logs out user, redirects to `/login`

---

## Favorites Route:

`/favorites`

Form to set user favorites, redirects to `/`

---

## Users Routes:

`/users/<user_id>`

Shows user profile

`/users/<user_id>/edit`

Form to edit logged in user's profile, redirects to `/users/<user_id>`

`/users/delete`

Deletes logged in users profile, redirects to `/signup`

---

## Match Routes:

`/matches`

Shows a list of the logged in users matched profiles

`/matches/<other_user_id>/delete`

Deletes a match between 2 users, redirects to `/matches`
