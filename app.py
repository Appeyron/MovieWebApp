"""
MovieWeb Application.

This module initializes the Flask application, establishes database routes,
and coordinates request handling between templates and the data manager.
"""

import os

from flask import Flask, abort, redirect, render_template, request, url_for
from sqlalchemy.exc import SQLAlchemyError

from data_manager import DataManager
from models import User, db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Save SQLite-database locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link database and app
db.init_app(app)

# Create object of DataManager class
data_manager = DataManager()


@app.route('/')
def index():
    """
    Render the home page.

    Fetch all registered application users and pass them to the main dashboard.
    """
    try:
        users = data_manager.get_users()
        return render_template('index.html', users=users)
    except SQLAlchemyError as e:
        print(f"Database error occurred on index page: {str(e)}")
        return "A database error occurred while fetching users.", 500


@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new application user.

    Receive the user name from a POST form, append it to the database record,
    and redirect back to the home page index.
    """
    name = request.form.get('name')
    if name:
        try:
            data_manager.create_user(name)
        except SQLAlchemyError as e:
            print(f"Database error occurred while creating user: {str(e)}")
            db.session.rollback()
            return "Could not add user due to a database error.", 500
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """
    Render a specific user's favorite movies list.

    Retrieve user details along with their corresponding movie entries,
    and render them in the specialized movie view template.
    """
    try:
        user = User.query.get_or_404(user_id)
        movies = data_manager.get_movies(user_id)
        return render_template('user_movies.html', movies=movies, user_id=user_id, user=user)
    except SQLAlchemyError as e:
        print(f"Database error occurred while fetching movies for user {user_id}: {str(e)}")
        return "Could not load the movie list due to a database issue.", 500


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """
    Add a movie to a user's collection.

    Look up a movie title requested via a form from the external OMDb API
    and bind it to the designated user profile.
    """
    title = request.form.get('title')
    if title:
        try:
            User.query.get_or_404(user_id)
            success = data_manager.add_movie(user_id, title)
            if not success:
                print(f"OMDb API error or movie not found for title: '{title}'")
        except SQLAlchemyError as e:
            print(f"Database error occurred while adding movie: {str(e)}")
            db.session.rollback()
            return "Could not add movie to favorites due to a database issue.", 500

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Modify attributes of an existing movie entry.

    Receive updated titles from user dashboard inputs and persist changes.
    """
    new_title = request.form.get('new_title')
    if new_title:
        try:
            success = data_manager.update_movie(movie_id, new_title)
            if not success:
                return abort(404, description="Movie record not found.")
        except SQLAlchemyError as e:
            print(f"Database error occurred while updating movie {movie_id}: {str(e)}")
            db.session.rollback()
            return "Could not update movie details.", 500

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Remove a movie from a user's collection.

    Locate a movie entry by its specific database primary ID and purge it.
    """
    try:
        success = data_manager.delete_movie(movie_id)
        if not success:
            return abort(404, description="Movie record not found.")
    except SQLAlchemyError as e:
        print(f"Database error occurred while deleting movie {movie_id}: {str(e)}")
        db.session.rollback()
        return "Could not delete movie from your list.", 500

    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 resource errors globally.

    Return an formatted HTTP 404 error page specifying the missing target context.
    """
    return f"<h1>404 Not Found</h1><p>{e.description}</p>", 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()
