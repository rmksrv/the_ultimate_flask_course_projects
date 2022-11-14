import dataclasses
import functools

import flask


def autoupdate_session(session_key):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            retval = func(self, *args, **kwargs)
            flask.session[session_key] = dataclasses.asdict(self)
            flask.session.modified = True
            return retval

        return wrapper

    return decorator
