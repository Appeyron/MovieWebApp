"""
Database Models Module.

Defines the SQLAlchemy schemas for the User and Movie entities
along with their relational mappings within the database.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):  # pylint: disable=too-few-public-methods
    """
    Represents an application user.

    Contains unique identifiers, profile attributes, and maintains
    a cascade-configured relationship linking to the user's movie collection.
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    # Unique constraint prevents creating identical users, improving robustness
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Allow access via `user.movies`
    # cascade="all, delete-orphan" ensures that if a user is deleted,
    # all their associated movies are automatically deleted from the DB too.
    movies = db.relationship(
        'Movie',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        """Provides a robust string representation for logging and debugging."""
        return f"<User {self.id}: {self.name}>"


class Movie(db.Model):  # pylint: disable=too-few-public-methods
    """
    Represents a favorite movie entry.

    Stores structured details fetched from the OMDb API and retains
    a foreign key mapping back to the owner's profile.
    """

    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(10), nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    poster = db.Column(db.String(500), nullable=True)

    # Link Movie to User
    # The foreign key links directly to the user table.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Provides a robust string representation for logging and debugging."""
        return f"<Movie {self.id}: '{self.title}' (User ID: {self.user_id})>"
