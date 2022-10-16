import abc
import dataclasses
import enum
from typing import ClassVar


class Deserializable(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, row: dict) -> "Deserializable":
        """Creates an instance from sqlite3 Row record"""


@dataclasses.dataclass(slots=True, eq=False)
class Question(Deserializable):
    id: int
    question: str
    asking_user_id: int
    expert_id: int
    answer: str | None = None

    _table_name: ClassVar[str] = "questions"

    def __eq__(self, other: "Question") -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_dict(cls, row: dict) -> "Question":
        return cls(
            id=row["id"],
            question=row["question"],
            asking_user_id=row["asking_user_id"],
            expert_id=row["expert_id"],
            answer=row["answer"],
        )


class UserPolicies(str, enum.Enum):
    ASKING_QUESTION = "asking_question"
    ANSWERING_QUESTIONS = "answering_questions"
    PROMOTING_TO_EXPERT = "promoting_to_expert"


class UserRole(str, enum.Enum):
    BASIC = "Basic"
    EXPERT = "Expert"
    ADMIN = "Admin"

    @property
    def policies(self) -> list[UserPolicies]:
        match self:
            case UserRole.BASIC:
                return [UserPolicies.ASKING_QUESTION]
            case UserRole.EXPERT:
                return [UserPolicies.ANSWERING_QUESTIONS]
            case UserRole.ADMIN:
                return [UserPolicies.ANSWERING_QUESTIONS, UserPolicies.PROMOTING_TO_EXPERT]
            case _:
                return []


@dataclasses.dataclass(slots=True, eq=False)
class User(Deserializable):
    id: int
    name: str
    password: str
    role: UserRole

    _table_name: ClassVar[str] = "users"

    def __eq__(self, other: "User") -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def from_dict(cls, row: dict) -> "User":
        return cls(
            id=row["id"],
            name=row["name"],
            password=row["password"],
            role=UserRole(row["role"]),
        )
