Gamr will use is the API from IGDB.com to get an updated list of all video games.
Users will be able to search through the list of videogames in the database and select their top 3 video games to add to their profiles.

####################################
Api Endpoint:

The endpoint my application will send requests to is: https://api.igdb.com/v4/games


axios({
  url: "https://api.igdb.com/v4/games",
  method: 'POST',
  headers: {
      'Accept': 'application/json',
      'Client-ID: Client ID',
      'Authorization: Bearer access_token',
  },
  data: "artworks,name,url;"
})
  .then(response => {
      console.log(response.data);
  })
  .catch(err => {
      console.error(err);
  });