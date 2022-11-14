import enum


class ExtendedEnum(enum.Enum):
    @classmethod
    def items(cls) -> list[tuple[str, str]]:
        return [(ref.name.lower(), ref.value) for ref in cls]  # type: ignore

    @classmethod
    def from_value(cls, value: str):
        for k, v in cls.__members__.items():
            if k.lower() == value.lower():
                return v
        else:
            raise ValueError(
                f"'{cls.__name__}' enum not found from value: '{value}'"
            )
