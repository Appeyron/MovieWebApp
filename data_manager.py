from models import db, User, Movie

class DataManager():
  # Define Crud operations as methods

  def create_user(self, name):
      new_user = User(name=name)
      db.session.add(new_user)
      db.session.commit()

get_users(self): Return a list of all users in your database.
get_movies(self, user_id): Return a list of all movies of a specific user.
add_movie(self, movie): Add a new movie to a user’s favorites. The process is similar to adding a new user.
You could fetch the OMDb movie information here in add_movie(self, title), in which case the second parameter would be only the title of the movie. You then have to add functionality for using the OMDb key.

update_movie(self, movie_id, new_title): Update the details of a specific movie in the database.
delete_movie(self, movie_id): Delete the movie from the user’s list of favorites.