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
    EqualTo,
    Email
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
    meal = StringField(
        "Meal",
        validators=[DataRequired()]
    )
    cuisine = StringField(
        "Cuisine",
        validators=[DataRequired()]
    )
    comment = TextAreaField(  # Comments are now optional
        "Comment",
        validators=[Optional()]
    )
    rating = IntegerField(
        "Rating",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=5)
        ]
    )
    website_link = StringField(  # Website URL is now optional
        "Website Link",
        validators=[
            Optional(),
            URL()
        ]
    )
    submit = SubmitField("Submit Review")


class ChangePasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password',
        validators=[
            DataRequired(),
            Length(min=6, message="Password must have at least 6 characters")
        ]
    )
    confirm_new_password = PasswordField(
        'Confirm New Password',
        validators=[
            DataRequired(),
            EqualTo('new_password', message="Passwords must match")
        ]
    )
    submit = SubmitField('Change Password')
