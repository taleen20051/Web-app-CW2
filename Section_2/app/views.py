from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, session, request, jsonify
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from .forms import LoginForm, RegisterForm, SearchForm, AddReviewForm
from .models import User, Restaurant, Review
from sqlalchemy.orm import joinedload
from app import db


# Generate a Flask Blueprint for grouping paths
app = Blueprint('app', __name__)


# Function to authenticate the user with a username and password
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return user
    return None


# Define the index route for the application (home page)
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('app.dashboard'))
    return render_template('index.html')


# Define the dashboard route for the application
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch all reviews with their associated users
    reviews = Review.query.options(joinedload(Review.user)).all()
    return render_template('dashboard.html', reviews=reviews)


# Define the register route for the application
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)

        # Check if username is taken, otherwise, proceed with registration
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "error")
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('app.login'))
    return render_template('register.html', form=form)


# Define the login route for the application
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Authenticate the user with the provided credentials
        user = authenticate_user(username, password)
        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('app.dashboard'))
        flash("Invalid username or password.", "error")
    return render_template('login.html', form=form)


# Add restaurant review card to the user's favorites
@app.route('/save/<int:restaurant_id>')
@login_required
def save_restaurant(restaurant_id):
    # Fetch the restaurant and check if it's already saved to user's favorites
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant not in current_user.saved_restaurants:
        current_user.saved_restaurants.append(restaurant)
        db.session.commit()
        flash('Restaurant saved!', 'success')
    else:
        flash('Restaurant already saved!', 'info')
    return redirect(url_for('app.dashboard'))


# User logout Route
@app.route('/logout')
@login_required
# Log out the user and remove the current user ID from session
def logout():
    logout_user()
    session.pop('user_id', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('app.login'))


# Search restaurants by cuisine
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = None
    # Check if the form is submitted
    if form.validate_on_submit():
        cuisine = form.cuisine.data
        location = form.location.data
        results = Restaurant.query.filter_by(
            cuisine=cuisine, location=location).all()
    return render_template('search.html', form=form, results=results)


# Input a new review into the database
@app.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = AddReviewForm()
    # Validate form submission and add the review to the database
    if form.validate_on_submit():
        review = Review(
            name=form.name.data,
            meal=form.meal.data,
            cuisine=form.cuisine.data,
            comment=form.comment.data,
            rating=form.rating.data,
            website_link=form.website_link.data,
            # Associate the review with the logged-in user
            user_id=current_user.id
        )
        db.session.add(review)
        db.session.commit()
        flash("Review added successfully!", "success")
        return redirect(url_for('app.dashboard'))
    return render_template('add_review.html', form=form)


# Update an existing review in the database
@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    form = AddReviewForm(obj=review)

    if form.validate_on_submit():
        # Update review fields with form data
        review.name = form.name.data
        review.meal = form.meal.data
        review.cuisine = form.cuisine.data
        review.comment = form.comment.data
        review.rating = form.rating.data
        review.website_link = form.website_link.data
        db.session.commit()
        flash('Your review has been updated.', 'success')
        return redirect(url_for('app.dashboard'))

    # Fill the form with pre-inserted data
    return render_template('add_review.html',
                           form=form, review=review, edit_mode=True)


# Route to add a review to favorites
@app.route('/add_to_favorites/<int:review_id>', methods=['POST'])
@login_required
def add_to_favorites(review_id):
    review = Review.query.get_or_404(review_id)
    # Check if review is already in favorites
    if review in current_user.favorites:
        return jsonify({"message": "Already in favorites"}), 200

    # Add to favorites otherwise
    current_user.favorites.append(review)
    db.session.commit()
    return jsonify({"message": "Added to favorites"}), 200


# Define the route to delete a review from favorites
@app.route('/remove_from_favorites/<int:review_id>', methods=['POST'])
@login_required
def remove_from_favorites(review_id):
    review = Review.query.get_or_404(review_id)

    # Check if the review is in the user's favorites and flash message
    if review in current_user.favorites:
        current_user.favorites.remove(review)
        db.session.commit()
        flash('Review removed from favorites.', 'success')
    else:
        flash('This review is not in your favorites.', 'info')

    return redirect(url_for('app.favorites'))


# Route to retrieve all reviews saved to favorites by the user
@app.route('/favorites')
@login_required
def favorites():
    favorites = current_user.favorites.all()
    return render_template('favorites.html', favorites=favorites)


# Route to view another user's profile page
@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    reviews = user.reviews
    return render_template('profile.html', user=user, reviews=reviews)


# Define the route to delete a review from the database
@app.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    # Ensure only the review's creator can delete it
    if review.user_id != current_user.id:
        flash("You are not authorized to delete this review.", "danger")
        return redirect(url_for('app.profile', username=current_user.username))

    db.session.delete(review)
    db.session.commit()
    flash("Review deleted successfully.", "success")
    return redirect(url_for('app.profile', username=current_user.username))


# Define the search results page route
@app.route('/search_results', methods=['GET'])
@login_required
def search_results():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template('search_results.html', reviews=[], query=query)

    # Filter reviews using case-insensitive search
    results = Review.query.filter(
        (Review.name.ilike(f"%{query}%")) |
        (Review.meal.ilike(f"%{query}%")) |
        (Review.cuisine.ilike(f"%{query}%"))
    ).all()

    return render_template('search_results.html', reviews=results, query=query)
