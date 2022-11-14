import werkzeug.datastructures

import store.constants
import store.forms
import store.models
import store.services.cart
from admin import constants


def unfinished_orders() -> list[store.models.Order]:
    return (
        store.models.Order
        .query
        .filter(
            store.models.Order.status != store.constants.OrderStatus.Delivered
        ).all()
    )


def finished_orders() -> list[store.models.Order]:
    return (
        store.models.Order
        .query
        .filter(
            store.models.Order.status == store.constants.OrderStatus.Delivered
        ).all()
    )


def order_by_id(id: int) -> store.models.Order | None:
    return store.models.Order.query.filter_by(id=id).first()


def new_product(
    name: str,
    price: int,
    stock: int,
    description: str,
    image: werkzeug.datastructures.FileStorage,
) -> store.models.Product:
    image_url = constants.UPLOAD_PHOTO_SET.url(
        constants.UPLOAD_PHOTO_SET.save(image)
    )
    product = store.models.Product(
        name=name,
        price=price,
        stock=stock,
        description=description,
        image=image_url,
    )
    store.models.db.session.add(product)
    store.models.db.session.commit()
    return product


def new_order(
    new_order_form: store.forms.SubmitNewOrderForm,
    cart: store.services.cart.Cart,
) -> store.models.Order:
    payment_type = store.constants.PaymentType.from_value(
        new_order_form.payment_type.data
    )
    shipping_type = store.constants.ShippingType.from_value(
        new_order_form.shipping_type.data
    )
    order = store.models.Order(
        reference=new_order_form.reference.data,
        first_name=new_order_form.first_name.data,
        last_name=new_order_form.last_name.data,
        phone_number=new_order_form.phone_number.data,
        email=new_order_form.email.data,
        address=new_order_form.address.data,
        city=new_order_form.city.data,
        state=new_order_form.state.data,
        country=new_order_form.country.data,
        status=store.constants.OrderStatus.Created,
        payment_type=payment_type,
        shipping_type=shipping_type,
    )
    for prod_cart, prod_model in cart.product_cart_model_pairs():
        order_item = store.models.OrderItems(
            product_id=prod_model.id,
            quantity=prod_cart.quantity,
        )
        order.items.append(order_item)
        prod_model.stock -= prod_cart.quantity
    store.models.db.session.add(order)
    store.models.db.session.commit()
    return order
