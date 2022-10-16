from typing import Iterable

import flask

import models


def logged_in_user(session: flask.session) -> models.User | None:
    user = session.get("logged_in_user")
    if isinstance(user, dict):
        user = models.User.from_dict(user)
    return user


def is_action_allowed_for_user(
    user: models.User | None,
    required_policies: Iterable[models.UserPolicies],
) -> bool:
    if not user:
        return False
    return all(policy in user.role.policies for policy in required_policies)
