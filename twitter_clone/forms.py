import flask_wtf
import flask_wtf.file
import flask_uploads
import wtforms

import constants


class RegisterForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        "Full Name",
        validators=[
            wtforms.validators.InputRequired("A full name is required"),
            wtforms.validators.Length(
                max=constants.UserConsts.MAX_NAME_LENGTH,
                message=(
                    f"Name can't be longer than "
                    f"{constants.UserConsts.MAX_NAME_LENGTH} symbols"
                ),
            ),
        ],
    )
    username = wtforms.StringField(
        "Username",
        validators=[
            wtforms.validators.InputRequired("Username is required"),
            wtforms.validators.Length(
                max=constants.UserConsts.MAX_USERNAME_LENGTH,
                message=(
                    f"Username can't be longer than "
                    f"{constants.UserConsts.MAX_USERNAME_LENGTH} symbols"
                ),
            ),
        ],
    )
    password = wtforms.StringField(
        "Password",
        validators=[
            wtforms.validators.InputRequired("Username is required"),
        ],
    )
    image = flask_wtf.file.FileField(
        validators=[
            flask_wtf.file.FileAllowed(
                flask_uploads.IMAGES, "Only images are accepted"
            ),
        ]
    )


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField(
        "Username",
        validators=[wtforms.validators.InputRequired("Username is required")],
    )
    password = wtforms.StringField(
        "Password",
        validators=[wtforms.validators.InputRequired("Enter a password")],
    )
    remember_me = wtforms.BooleanField("Remember me")


class NewTweetForm(flask_wtf.FlaskForm):
    text = wtforms.TextAreaField(
        "Text",
        validators=[
            wtforms.validators.InputRequired("Enter the tweet's text"),
            wtforms.validators.Length(
                max=constants.TweetConsts.MAX_TEXT_LENGTH
            ),
        ],
    )
