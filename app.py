from flask import Flask, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User  # Added User import

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# save SQLite-database locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link database and app
db.init_app(app)

# # create tables if not existent
# with app.app_context():
#     db.create_all()

# create object of DataManager class
data_manager = DataManager()


@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


@app.route('/users', methods=['GET'])
def list_users():
    """Show a list of all registered users and a form for adding new users."""
    users = data_manager.get_users()

    # Temporarily returning users as HTML string for testing
    user_list = "".join([f"<li><a href='/users/{u.id}/movies'>{u.name}</a></li>" for u in users])
    return f"""
        <h1>Movie Web App - Users</h1>
        <ul>{user_list}</ul>
        <h3>Add a new user:</h3>
        <form action="/users" method="POST">
            <input type="text" name="name" placeholder="User Name" required>
            <button type="submit">Add User</button>
        </form>
    """


@app.route('/users', methods=['POST'])
def add_user():
    """Receive the new user info, add it to the database, then redirect back to /users."""
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('list_users'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Retrieve that user’s list of favorite movies and display it."""
    movies = data_manager.get_movies(user_id)

    # Temporarily rendering movie list and action forms as HTML string
    movie_list = ""
    for m in movies:
        movie_list += f"""
            <li>
                <strong>{m.title}</strong> ({m.year}) - Rating: {m.rating} <br>
                <img src="{m.poster}" width="100"><br>
                <form action="/users/{user_id}/movies/{m.id}/update" method="POST" style="display:inline;">
                    <input type="text" name="new_title" placeholder="New Title" required>
                    <button type="submit">Update Title</button>
                </form>
                <form action="/users/{user_id}/movies/{m.id}/delete" method="POST" style="display:inline;">
                    <button type="submit" style="color:red;">Delete</button>
                </form>
            </li>
            <hr>
        """

    return f"""
        <h1>Favorite Movies for User ID: {user_id}</h1>
        <ul>{movie_list}</ul>
        <h3>Add a new movie via OMDb:</h3>
        <form action="/users/{user_id}/movies" method="POST">
            <input type="text" name="title" placeholder="Movie Title" required>
            <button type="submit">Add Movie</button>
        </form>
        <p><a href="/users">Back to Users</a></p>
    """


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
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


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()