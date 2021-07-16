1. What goal will your website be designed to achieve?

  Gamr is designed to make it easier for gamers to find other gamers to play with by matching them together.

2. What kind of users will visit your site? In other words, what is the demographic of
your users?

  The target demographic for Gamr is anyone who plays video games and is looking for others to play with.

3. What data do you plan on using? You may have not picked your actual API yet,
which is fine, just outline what kind of data you would like it to contain.

  Gamr pulls video game data from a database so users can select their favorite games to attach to their profiles.

4. In brief, outline your approach to creating your project (knowing that you may not
know everything in advance and that these details might change later). Answer
questions like the ones below, but feel free to add more information:

a. What does your database schema look like?

  Gamr's database schema will have a table of users, a table of matched users, and a table of user's favorite games.

b. What kinds of issues might you run into with your API?

  The API used will have to be up to date. Popularity of various video games is constantly changing as new games release.

c. Is there any sensitive information you need to secure?

  User's password will be encrypted. User's discord username and email address will be hidden unless matched.

d. What functionality will your app include?

  - Create user accounts/profiles
  - User login
  - Edit User profile
  - Delete User profile
  - Display other user profiles
  - Accept or dismiss other profiles
  - Match users
  - Display a list of matched profiles that reveals email addresses and optionally discord usernames so matched players can connect.

e. What will the user flow look like?

  Users will sign up for an account or log in.
  Gamr will display another user's public profile to the user and allow them to accept or dismiss the match.
  If dismissed it will show another profile until they approve a match.
  Once a user approves a profile it will go into the match table of the database.
  The other user will then see the first user's profile, as if it was random, and approve or dismiss the match.
  If they dismiss, adds a False value to the match table and will no longer show eachother respective profiles.
  If they approve, adds a True value to the match table and the users will be notified they are a match.
  Once 2 users are matched they will have the ability to see each others discord usernames and email addresses to connect and plan a game session.

f. What features make your site more than CRUD? Do you have any stretch
goals?

  Gamr's matching feature makes it more than CRUD.
  Stretch goals:
    Add chat functionality within the application
    Integrate a CICD pipeline
    Code quality and maintainability integration
    Deploy the application using Heroku
