from store import models


def product_by_id(id: int) -> models.Product | None:
    return models.Product.query.filter_by(id=id).first()


def available_products() -> list[models.Product]:
    return models.Product.query.filter(models.Product.stock > 0).all()


def out_of_stock_products() -> list[models.Product]:
    return models.Product.query.filter(models.Product.stock == 0).all()
