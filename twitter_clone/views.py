import datetime

import flask
import flask_login
import werkzeug.security

import constants
import forms
import models
from app import (
    app,
    db,
    upload_photos_set,
)


def who_to_watch_suggestions(user: models.User) -> list[models.User]:
    return (
        models.User.query.order_by(db.func.random())
        .filter(models.User.id != user.id)
        .limit(constants.AMOUNT_OF_WHO_TO_WATCH_REFS)
        .all()
    )


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    login_form = forms.LoginForm()
    return flask.render_template(
        "index.html",
        login_form=login_form,
    )


@app.route("/login", methods=["POST"])
def login() -> str | flask.Response:
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        found_user = models.User.query.filter_by(
            username=login_form.username.data
        ).first()

        if not found_user:
            return flask.render_template(
                "index.html",
                login_form=login_form,
                message="No such user exists",
            )

        if werkzeug.security.check_password_hash(
            found_user.password, login_form.password.data
        ):
            flask_login.login_user(found_user)
            return flask.redirect(flask.url_for("profile"))  # type: ignore
        return flask.render_template(
            "index.html", login_form=login_form, message="Invalid password"
        )
    return flask.render_template(
        "index.html",
        login_form=login_form,
    )


@app.route("/logout")
@flask_login.login_required
def logout() -> flask.Response:
    flask_login.logout_user()
    return flask.redirect(flask.url_for("index"))  # type: ignore


@app.route("/profile", defaults={"username": None})
@app.route("/profile/<username>")
@flask_login.login_required
def profile(username: str | None) -> str:
    if username:
        user: models.User = models.User.query.filter_by(username=username).first()
    else:
        user: models.User = flask_login.current_user  # type: ignore
    if not user:
        flask.abort(404)
    tweets = (
        models.Tweet.query.filter_by(author=user)
        .order_by(models.Tweet.created_at.desc())
        .all()
    )
    who_to_watch = who_to_watch_suggestions(user)
    current_time = datetime.datetime.utcnow()
    return flask.render_template(
        "profile.html",
        user=user,
        tweets=tweets,
        who_to_watch=who_to_watch,
        current_time=current_time,
    )


@app.route("/timeline", defaults={"username": None})
@app.route("/timeline/<username>")
@flask_login.login_required
def timeline(username: str | None) -> str:
    new_tweet_form = forms.NewTweetForm()
    if username:
        user: models.User = models.User.query.filter_by(username=username).first()
    else:
        user: models.User = flask_login.current_user  # type: ignore
    if not user:
        flask.abort(404)
    tweets = (
        models.Tweet.query.filter(
            models.Tweet.author_id.in_([following.id for following in user.following])
        )
        .order_by(models.Tweet.created_at.desc())
        .all()
    )
    who_to_watch = who_to_watch_suggestions(user)
    current_time = datetime.datetime.utcnow()
    return flask.render_template(
        "timeline.html",
        user=user,
        tweets=tweets,
        who_to_watch=who_to_watch,
        current_time=current_time,
        new_tweet_form=new_tweet_form,
    )


@app.route("/post-tweet", methods=["POST"])
@flask_login.login_required
def post_tweet():
    new_tweet_form = forms.NewTweetForm()
    if new_tweet_form.validate():
        new_tweet = models.Tweet(
            author_id=flask_login.current_user.id,
            text=new_tweet_form.text.data,
        )
        db.session.add(new_tweet)
        db.session.commit()
    return flask.redirect(flask.url_for("timeline"))


@app.route("/register", methods=["GET", "POST"])
def register() -> str | flask.Response:
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        password_hash = werkzeug.security.generate_password_hash(
            register_form.password.data
        )
        uploaded_image_filename = upload_photos_set.save(register_form.image.data)
        uploaded_image_url = upload_photos_set.url(uploaded_image_filename)
        new_user = models.User(
            username=register_form.username.data,
            password=password_hash,
            name=register_form.name.data,
            image=uploaded_image_url,
        )
        db.session.add(new_user)
        db.session.commit()
        flask_login.login_user(new_user)
        return flask.redirect(flask.url_for("profile"))  # type: ignore
    return flask.render_template(
        "register.html",
        register_form=register_form,
    )


@app.route("/follow/<username>")
@flask_login.login_required
def follow(username: str) -> flask.Response:
    user_to_follow = models.User.query.filter_by(username=username).first()
    if not user_to_follow:
        flask.abort(404)
    flask_login.current_user.following.append(user_to_follow)
    db.session.commit()
    return flask.redirect(flask.url_for("profile", username=username))  # type: ignore
