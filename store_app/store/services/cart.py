import dataclasses

import flask

import utils
from store import (
    models,
    services,
)


@dataclasses.dataclass(slots=True)
class ProductInCart:
    id: int
    quantity: int

    @property
    def total_price(self):
        price = services.product.product_by_id(self.id).price  # type: ignore
        return price * self.quantity

    def pair_with_model(self) -> tuple["ProductInCart", models.Product]:
        return self, services.product.product_by_id(self.id)

    def __eq__(self, other):
        if isinstance(other, dict):
            other = ProductInCart.from_dict(other)
        return self.id == other.id

    @classmethod
    def from_dict(cls, d: dict):
        return cls(id=d["id"], quantity=d["quantity"])


@dataclasses.dataclass(slots=True)
class Cart:
    products: list[ProductInCart] = dataclasses.field(default_factory=list)

    @property
    def total_price(self):
        return sum(p.total_price for p in self.products)

    def __len__(self) -> int:
        return sum(p.quantity for p in self.products)

    def __repr__(self) -> str:
        return f"Cart({self.products})"

    @utils.flask.autoupdate_session("cart")
    def clear(self) -> None:
        self.products.clear()

    @utils.flask.autoupdate_session("cart")
    def add(self, product: ProductInCart) -> None:
        if product in self.products:
            # looks like I ain't feeling nice
            i = self.products.index(product)
            self.products[i].quantity += product.quantity
        else:
            self.products.append(product)

    @utils.flask.autoupdate_session("cart")
    def remove(self, product_id: int) -> None:
        for product in self.products:
            if product.id == product_id:
                self.products.remove(product)

    @classmethod
    def from_session(cls):  # type: ignore
        cart_dict = flask.session.get("cart")
        if not cart_dict:
            cart = cls()
            flask.session["cart"] = dataclasses.asdict(cart)
        else:
            products = [
                ProductInCart.from_dict(prod_dict)
                for prod_dict in cart_dict.get("products")
            ]
            cart = cls(products=products)
        return cart

    def product_cart_model_pairs(
        self,
    ) -> list[tuple[ProductInCart, models.Product]]:
        res = []
        for product in self.products:
            res.append(product.pair_with_model())
        return res
