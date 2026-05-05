from app.models.pizza_ingredient import Pizza, PizzaPublicWithSize, PizzaSize
from app.models.restaurant_models import Pizza


def pizza_with_size(pizza: Pizza, pizza_size: PizzaSize) -> PizzaPublicWithSize:
    return PizzaPublicWithSize(
        id=pizza.id,
        name=pizza.name,
        description=pizza.description,
        small_price=pizza.small_price,
        medium_price=pizza.medium_price,
        large_price=pizza.large_price,
        size=pizza_size,
        spiciness=pizza.spiciness,
        vegetarian=pizza.vegetarian,
    )
