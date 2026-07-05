import os
import requests
from dotenv import load_dotenv
from models import db, User, Movie

# Load environment variables from the .env file
load_dotenv()


class DataManager:
    def __init__(self):
        # Fetch the API key from the environment variables
        self.api_key = os.getenv("OMDB_API_KEY")

        # Optional: Safety check during development
        if not self.api_key:
            raise ValueError("API Key missing! Please check your .env file.")

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self):
        """Return a list of all users in your database."""
        return User.query.all()

    def get_movies(self, user_id):
        """Return a list of all movies of a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, title):
        """Fetch the OMDb movie information and add a new movie to a user's favorites."""
        url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={title}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data.get("Response") == "True":
                new_movie = Movie(
                    title=data.get("Title"),
                    year=data.get("Year"),
                    rating=data.get("imdbRating"),
                    poster=data.get("Poster"),
                    user_id=user_id
                )
                db.session.add(new_movie)
                db.session.commit()
                return True
        return False

    def update_movie(self, movie_id, new_title):
        """Update the details of a specific movie in the database."""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
            return True
        return False

    def delete_movie(self, movie_id):
        """Delete the movie from the user's list of favorites."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False