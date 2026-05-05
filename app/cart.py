from sqlmodel import Session, select

from app.models.pizza_ingredient import Pizza, PizzaSize
from app.models.restaurant_models import Cart, CartPizza


def get_cart(session: Session, session_id: str) -> Cart:
    cart = session.exec(select(Cart).where(Cart.session_id == session_id)).one_or_none()

    if cart:
        return cart

    cart = Cart(session_id=session_id)

    session.add(cart)
    session.commit()
    session.refresh(cart)

    return cart


def add_to_cart(
    session: Session, cart: Cart, pizza: Pizza, pizza_size: PizzaSize
) -> Pizza | None:
    cart_pizza = CartPizza(cart=cart, pizza=pizza, pizza_size=pizza_size)
    cart.cart_pizzas.append(cart_pizza)

    session.add(cart_pizza)
    session.commit()
    session.refresh(cart)

    return cart_pizza


def remove_from_cart(
    session: Session, cart: Cart, pizza: Pizza, pizza_size: PizzaSize
) -> bool:
    cart_pizza = session.exec(
        select(CartPizza)
        .where(CartPizza.cart == cart)
        .where(CartPizza.pizza == pizza)
        .where(CartPizza.pizza_size == pizza_size)
    ).all()

    if not cart_pizza:
        return False

    session.delete(cart_pizza[0])
    session.commit()

    return True
