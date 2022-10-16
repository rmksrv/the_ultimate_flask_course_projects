import models
import repos.user


def promote_user_to_expert(user: models.User) -> None:
    updating_data = {
        "role": models.UserRole.EXPERT
    }
    repos.user.change(updating_data=updating_data, user=user)


def is_user_with_nickname_exists(nickname: str) -> bool:
    try_user = repos.user.one_of(name=nickname)
    return try_user is not None
