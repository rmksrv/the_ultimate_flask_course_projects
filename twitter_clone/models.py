import datetime

import flask_login

import constants
from app import db, login_manager


followers = db.Table(
    "follower",
    db.Column("follower_id", db.ForeignKey("user.id")),
    db.Column("followee_id", db.ForeignKey("user.id")),
)


class User(db.Model, flask_login.UserMixin):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(constants.UserConsts.MAX_USERNAME_LENGTH))
    password = db.Column(db.String(constants.UserConsts.MAX_PASSWORD_LENGTH))
    name = db.Column(db.String(constants.UserConsts.MAX_NAME_LENGTH))
    image = db.Column(db.String(constants.UserConsts.MAX_IMAGE_LENGTH))
    joined_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    tweets = db.relationship("Tweet", backref="author", lazy="dynamic")
    following = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followee_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )


class Tweet(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(constants.TweetConsts.MAX_TEXT_LENGTH))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)
