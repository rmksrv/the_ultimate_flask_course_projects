import enum
import pathlib


# Common
SECRET_KEY = "some_non_prod_secret"
DEBUG = True
PROJECT_ROOT = pathlib.Path(__file__).parent
DATABASE_URI = (
    "sqlite:////Users/rmksrv/PycharmProjects/"
    "the_ultimate_flask_course/twitter_clone/"
    "twitter_clone_db.sqlite"
)


# File uploads
UPLOADED_IMAGES_PATH = PROJECT_ROOT / "images"


# Models
class UserConsts(enum.IntEnum):
    MAX_USERNAME_LENGTH = 30
    MAX_PASSWORD_LENGTH = 50
    MAX_NAME_LENGTH = 100
    MAX_IMAGE_LENGTH = 100


class TweetConsts(enum.IntEnum):
    MAX_TEXT_LENGTH = 255


AMOUNT_OF_TIMELINE_POSTS = 10
AMOUNT_OF_WHO_TO_WATCH_REFS = 4
