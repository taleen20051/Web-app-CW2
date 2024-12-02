from app import db
from flask_login import UserMixin
from datetime import datetime

# Define association table for a many-to-many relationship (users and reviews)
favorites = db.Table(
    'favorites',
    # Define a column for the user ID
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True
    ),
    # Define a column for the review ID
    db.Column(
        'review_id',
        db.Integer,
        db.ForeignKey('review.id'),
        primary_key=True
    )
)


# User model for managing user's review data
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)
    # Many-to-many relationship for favorites
    favorites = db.relationship(
     'Review',
     secondary=favorites,
     backref=db.backref('favorited_by', lazy='dynamic')
    )


# Restaurant model for storing restaurant data
class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Review model for storing user reviews of restaurants
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    meal = db.Column(db.String(80), nullable=False)
    cuisine = db.Column(db.String(80), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    website_link = db.Column(db.String(200), nullable=True)
    # Foreign key linking the review to a specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
