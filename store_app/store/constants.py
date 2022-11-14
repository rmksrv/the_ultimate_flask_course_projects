import enum
import pathlib

import utils


APP_NAME = "store"
PROJECT_ROOT = pathlib.Path.cwd().parent
APP_ROOT = PROJECT_ROOT / APP_NAME
TEMPLATES_PATH = "templates"
STATIC_PATH = "static"


class References(utils.common.ExtendedEnum):
    Mr = "Mr"
    Mrs = "Mrs"
    Miss = "Miss"


class OrderStatus(enum.Enum):
    Created = "Created"
    Assembling = "Assembling"
    InDelivery = "In Delivery"
    Delivered = "Delivered"


class PaymentStatus(enum.Enum):
    PAID = "Paid"
    NOT_PAID = "Not paid"


class PaymentType(utils.common.ExtendedEnum):
    CreditCardPayment = "Credit Card Payment"
    CODPayment = "Cash On Delivery"


class ShippingType(utils.common.ExtendedEnum):
    Shipping24Hr = "24hr Shipping"
    ShippingOneWeek = "One week Shipping"
