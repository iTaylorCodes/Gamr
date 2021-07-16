####################################
Homepage:

@app.route('/')
"""
Shows the homepage.
If logged in:
Shows another users profile card with an accept or dismiss button
Else:
Returns a 'home' template that describes Gamr with a link to signup.
"""

####################################
Users Routes:

@app.route('/users/<int:user_id>')
"""Shows user profile"""

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
"""A form to edit logged in user's profile"""

@app.route('/users/delete', methods=["POST"])
"""Deletes logged in users profile and redirects to /signup"""

@app.route('/users/<int:user_id>/matches)
"""Shows a list of matched profiles"""

@app.route('/users/<int:user_id>/matches/<int:match_id>/delete, methods=["POST"])
"""Deletes a match"""

####################################
Signup/Login/Logout Routes:

@app.route('/signup', methods=["GET", "POST"])
"""A form to create a new account"""

@app.route('/login', methods=["GET", "POST"])
"""A form to login"""

@app.route('/logout')
"""Logs out user and redirects to /login"""

####################################

<!-- If I'm able to implement a chat functionality within the application* -->

Chat Route:

@app.route('/users/<int:user_id>/matches/<int:match_id>/chat)
"""Displays a chat between matched users"""
