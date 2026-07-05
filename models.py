from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
  # Define all the Movie properties

  # Link Movie to User
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
