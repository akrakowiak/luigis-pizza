import uuid
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.cart import add_to_cart as add_to_cart_instance
from app.cart import get_cart
from app.cart import remove_from_cart as remove_from_cart_instance
from app.db import SessionDep
from app.models.pizza_ingredient import (
    Pizza,
    PizzaPublicWithIngredients,
    PizzaPublicWithSize,
    PizzaSize,
)
from app.models.restaurant_models import Cart
from app.pizza import pizza_with_size
from app.session import get_session

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=list[PizzaPublicWithSize])
async def read_cart(
    session: SessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
):
    session_instance, created = get_session(session, session_id)
    if created:
        response.set_cookie(key="session_id", value=session_instance.id)

    cart = get_cart(session, session_instance.id)

    cart_pizzas = [
        pizza_with_size(cart_pizza.pizza, cart_pizza.pizza_size)
        for cart_pizza in cart.cart_pizzas
    ]
    print(cart_pizzas)
    return cart_pizzas


class PizzaIdSize(BaseModel):
    pizza_id: str
    pizza_size: PizzaSize


@router.post("/", response_model=list[PizzaPublicWithSize])
async def add_to_cart(
    pizza_id_size: PizzaIdSize,
    session: SessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
):
    pizza_id = pizza_id_size.pizza_id
    pizza_size = pizza_id_size.pizza_size

    pizza = session.get(Pizza, pizza_id)

    if not pizza:
        raise HTTPException(status_code=404, detail="pizza not found")

    session_instance, created = get_session(session, session_id)
    if created:
        response.set_cookie(key="session_id", value=session_instance.id)

    cart = get_cart(session, session_instance.id)
    added_pizza = add_to_cart_instance(session, cart, pizza, pizza_size)

    cart_pizzas = [
        pizza_with_size(cart_pizza.pizza, cart_pizza.pizza_size)
        for cart_pizza in cart.cart_pizzas
    ]
    return cart_pizzas


@router.delete("/")
async def remove_from_cart(
    pizza_id_size: PizzaIdSize,
    session: SessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
):
    pizza_id = pizza_id_size.pizza_id
    pizza_size = pizza_id_size.pizza_size

    pizza = session.get(Pizza, pizza_id)

    if not pizza:
        raise HTTPException(status_code=404, detail="pizza not found")

    session_instance, created = get_session(session, session_id)
    if created:
        response.set_cookie(key="session_id", value=session_instance.id)

    cart = get_cart(session, session_instance.id)
    is_pizza_removed = remove_from_cart_instance(session, cart, pizza, pizza_size)

    if not is_pizza_removed:
        raise HTTPException(status_code=404, detail="pizza not found in cart")
