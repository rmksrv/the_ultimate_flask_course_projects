import flask_uploads
import flask_wtf
import flask_wtf.file
import wtforms


class AddProductForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        "Name",
        validators=[wtforms.validators.InputRequired("Name is required")],
    )
    price = wtforms.IntegerField(
        "Price",
        validators=[
            wtforms.validators.InputRequired("Price is required"),
            wtforms.validators.NumberRange(min=0),
        ],
    )
    stock = wtforms.IntegerField(
        "Stock",
        validators=[
            wtforms.validators.InputRequired("Stock is required"),
            wtforms.validators.NumberRange(min=0),
        ],
    )
    description = wtforms.TextAreaField("Description")
    image = flask_wtf.file.FileField(
        "Image",
        validators=[
            flask_wtf.file.FileAllowed(
                flask_uploads.IMAGES, "Only images allowed"
            ),
        ],
    )
