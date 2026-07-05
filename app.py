from flask import Flask, request, redirect, url_for, render_template
from data_manager import DataManager
from models import db, Movie, User

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# save SQLite-database locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link database and app
db.init_app(app)

# create object of DataManager class
data_manager = DataManager()


@app.route('/')
def index():
    """The home page of your application. Fetch and pass the list of users to the template."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Receive the new user info, add it to the database, then redirect back to home."""
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Retrieve that user’s details and their list of favorite movies, then display it."""
    # 1. Fetch the user object using the user_id
    user = User.query.get_or_404(user_id)

    # 2. Fetch the movies for this user
    movies = data_manager.get_movies(user_id)

    # 3. Pass the 'user' object to the template
    return render_template('user_movies.html', movies=movies, user_id=user_id, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies via OMDb API."""
    title = request.form.get('title')
    if title:
        data_manager.add_movie(user_id, title)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list."""
    new_title = request.form.get('new_title')
    if new_title:
        data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()