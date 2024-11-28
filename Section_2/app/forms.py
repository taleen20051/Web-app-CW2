from flask_wtf import FlaskForm
from wtforms import (  # noqa: F401
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    IntegerField,
    URLField
)
from wtforms.validators import (  # noqa: F401
    DataRequired,
    Length,
    NumberRange,
    URL,
    Optional,
    EqualTo
)


# Define the login form class with the required fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Define the registration form class with the required fields and validators
class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Register')


# Define the search class with the required fields
class SearchForm(FlaskForm):
    cuisine = StringField('Cuisine', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Search')


# Define the add review form class with the required fields and validators
class AddReviewForm(FlaskForm):
    name = StringField(
        "Restaurant Name",
        validators=[DataRequired()]
    )
    # Meal field with a required validator
    meal = StringField(
        "Meal",
        validators=[DataRequired()]
    )
    # Cuisine field with a required validator
    cuisine = StringField(
        "Cuisine",
        validators=[DataRequired()]
    )
    # Comments field with a required validator
    comment = TextAreaField(
        "Comment",
        validators=[DataRequired()]
    )
    # Rating field with a required validator (1-5)
    rating = IntegerField(
        "Rating",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=5)
        ]
    )
    # Website URL field with a required validator
    website_link = StringField(
        "Website Link",
        validators=[
            DataRequired(),
            URL()
        ]
    )
    # Submit button for the form
    submit = SubmitField("Submit Review")