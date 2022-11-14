import flask_wtf
import wtforms

from store import constants


class AddProductToCartForm(flask_wtf.FlaskForm):
    id = wtforms.IntegerField("ID", widget=wtforms.widgets.HiddenInput())
    quantity = wtforms.IntegerField(
        "Quantity",
        validators=[
            wtforms.validators.InputRequired("Quantity is required"),
            wtforms.validators.NumberRange(min=0),
        ],
    )


class SubmitNewOrderForm(flask_wtf.FlaskForm):
    reference = wtforms.SelectField(
        "Title",
        choices=constants.References.items(),
        validators=[wtforms.validators.InputRequired("required")],
    )
    first_name = wtforms.StringField(
        "First Name",
        validators=[wtforms.validators.InputRequired("required")],
    )
    last_name = wtforms.StringField(
        "Last Name",
        validators=[wtforms.validators.InputRequired("required")],
    )
    phone_number = wtforms.TelField(
        "Phone number",
        validators=[wtforms.validators.InputRequired("required")],
    )
    email = wtforms.EmailField(
        "Email",
        validators=[wtforms.validators.InputRequired("required")],
    )
    address = wtforms.StringField(
        "Address",
        validators=[wtforms.validators.InputRequired("required")],
    )
    city = wtforms.StringField(
        "City",
        validators=[wtforms.validators.InputRequired("required")],
    )
    state = wtforms.StringField(
        "State",
        validators=[wtforms.validators.InputRequired("required")],
    )
    country = wtforms.StringField(
        "Country",
        validators=[wtforms.validators.InputRequired("required")],
    )
    payment_type = wtforms.SelectField(
        "Payment type",
        choices=constants.PaymentType.items(),
        validators=[wtforms.validators.InputRequired("required")],
    )
    shipping_type = wtforms.SelectField(
        "Shipping type",
        choices=constants.ShippingType.items(),
        validators=[wtforms.validators.InputRequired("required")],
    )
    agree_with_tos = wtforms.BooleanField(
        "I agree to the terms of service.",
        validators=[wtforms.validators.DataRequired()],
    )
