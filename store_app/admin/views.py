import flask
import flask.typing as ftypes

import store.services
from admin import (
    admin_blueprint,
    forms,
    service,
)


@admin_blueprint.route("/")
def admin() -> ftypes.ResponseReturnValue:
    return flask.render_template(
        "admin/index.html",
        is_admin=True,  # TODO: remove
        available_products=store.services.product.available_products(),
        out_of_stock_products=store.services.product.out_of_stock_products(),
        unfinished_orders=service.unfinished_orders(),
        finished_orders=service.finished_orders(),
        cart=store.services.cart.Cart.from_session(),
    )


@admin_blueprint.route("/add", methods=["GET", "POST"])
def add() -> ftypes.ResponseReturnValue:
    add_product_form = forms.AddProductForm()
    if add_product_form.validate_on_submit():
        service.new_product(
            name=add_product_form.name.data,
            price=add_product_form.price.data,  # type: ignore
            stock=add_product_form.stock.data,  # type: ignore
            description=add_product_form.description.data,
            image=add_product_form.image.data,
        )
        return flask.redirect(flask.url_for("admin.admin"))

    return flask.render_template(
        "admin/add-product.html",
        is_admin=True,  # TODO: remove
        add_product_form=add_product_form,
        cart=store.services.cart.Cart.from_session(),
    )


@admin_blueprint.route("/order/<id>")
def order(id: int) -> ftypes.ResponseReturnValue:
    return flask.render_template(
        "admin/view-order.html",
        is_admin=True,  # TODO: remove
        cart=store.services.cart.Cart.from_session(),
        order=service.order_by_id(id),
    )
