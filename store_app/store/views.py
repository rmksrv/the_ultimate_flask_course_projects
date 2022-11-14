import flask
import flask.typing as ftypes

import admin.service
from store import (
    forms,
    store_blueprint,
    services,
)


# TODO: remove when ready
@store_blueprint.route("/clear")
def clear() -> ftypes.ResponseReturnValue:
    flask.session.clear()
    return flask.redirect(flask.url_for("store.index"))


@store_blueprint.route("/")
def index() -> ftypes.ResponseReturnValue:
    return flask.render_template(
        "store/index.html",
        available_products=services.product.available_products(),
        out_of_stock_products=services.product.out_of_stock_products(),
    )


@store_blueprint.route("/product/<id>")
def product(id: int) -> ftypes.ResponseReturnValue:
    add_product_to_cart_form = forms.AddProductToCartForm()
    return flask.render_template(
        "store/view-product.html",
        product=services.product.product_by_id(id),
        add_product_to_cart_form=add_product_to_cart_form,
    )


@store_blueprint.route("/cart")
def cart() -> ftypes.ResponseReturnValue:
    cart = services.cart.Cart.from_session()
    return flask.render_template(
        "store/cart.html",
        cart=cart,
        shipping=services.shipping.Shipping24Hr(cart),
    )


@store_blueprint.route("/checkout", methods=["GET", "POST"])
def checkout() -> ftypes.ResponseReturnValue:
    submit_new_order_form = forms.SubmitNewOrderForm()
    cart = services.cart.Cart.from_session()
    if submit_new_order_form.validate_on_submit():
        admin.service.new_order(submit_new_order_form, cart)
        cart.clear()
        return flask.redirect(flask.url_for("store.index"))
    return flask.render_template(
        "store/checkout.html",
        submit_new_order_form=submit_new_order_form,
        cart=cart,
        shipping=services.shipping.Shipping24Hr(cart),
    )


@store_blueprint.route("/add-product-to-cart", methods=["POST"])
def add_product_to_cart() -> ftypes.ResponseReturnValue:
    add_product_to_cart_form = forms.AddProductToCartForm()
    if add_product_to_cart_form.validate_on_submit():
        product_in_cart = services.cart.ProductInCart(
            id=int(add_product_to_cart_form.id.data),  # type: ignore
            quantity=add_product_to_cart_form.quantity.data,  # type: ignore
        )
        services.cart.Cart.from_session().add(product_in_cart)
    return flask.redirect(flask.url_for("store.index"))


@store_blueprint.route("/quick-add-to-cart/<id>")
def quick_add_to_cart(id: int) -> ftypes.ResponseReturnValue:
    product_in_cart = services.cart.ProductInCart(id=int(id), quantity=1)
    services.cart.Cart.from_session().add(product_in_cart)
    return flask.redirect(flask.url_for("store.index"))


@store_blueprint.route("/remove-product-from-cart/<id>")
def remove_product_from_cart(id: int) -> ftypes.ResponseReturnValue:
    services.cart.Cart.from_session().remove(int(id))
    return flask.redirect(flask.url_for("store.cart"))
