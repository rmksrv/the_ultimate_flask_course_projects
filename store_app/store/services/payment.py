import abc
import dataclasses
import typing as t

from store import constants


@dataclasses.dataclass
class BasePayment(abc.ABC):
    name: t.ClassVar[str]

    @abc.abstractmethod
    def pay(self) -> constants.PaymentStatus:
        ...

    def __repr__(self) -> str:
        return self.name


@dataclasses.dataclass(slots=True)
class CreditCardPayment(BasePayment):
    name = constants.PaymentType.CreditCardPayment.value

    def pay(self) -> constants.PaymentStatus:
        return constants.PaymentStatus.PAID


@dataclasses.dataclass(slots=True)
class CODPayment(BasePayment):
    name = constants.PaymentType.CODPayment.value

    def pay(self) -> constants.PaymentStatus:
        return constants.PaymentStatus.NOT_PAID
