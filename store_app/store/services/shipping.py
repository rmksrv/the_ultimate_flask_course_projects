import abc
import dataclasses
import typing as t

from store import (
    services,
    constants
)


@dataclasses.dataclass(slots=True)
class BaseShipping(abc.ABC):
    cart: services.cart.Cart
    name: t.ClassVar[str]

    @property
    @abc.abstractmethod
    def price(self):
        """Calculates price of shipping"""

    def __repr__(self) -> str:
        return self.name


def from_value(
    val: str | constants.ShippingType,
    cart: services.cart.Cart | None = None
) -> BaseShipping:
    if isinstance(val, str):
        val = constants.ShippingType.from_value(val)
    for shipping_cls in BaseShipping.__subclasses__():
        if shipping_cls.name == val.value:
            return shipping_cls(cart=cart)
    else:
        raise ValueError(
            f"Shipping not found from value: '{val}'"
        )


class Shipping24Hr(BaseShipping):
    name = constants.ShippingType.Shipping24Hr.value

    @property
    def price(self):
        return 40


class ShippingOneWeek(BaseShipping):
    name = constants.ShippingType.ShippingOneWeek.value

    @property
    def price(self):
        return 15
