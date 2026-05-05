from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db import SessionDep
from app.models.pizza_ingredient import (
    Pizza,
    PizzaCreate,
    PizzaPublicWithIngredients,
    PizzaUpdate,
)

router = APIRouter(
    prefix="/pizzas",
    tags=["pizzas"],
)


@router.post("/")
async def create_pizza(pizza_create: PizzaCreate, session: SessionDep):
    pizza = Pizza(**pizza_create.dict())

    session.add(pizza)
    session.commit()
    session.refresh(pizza)

    return pizza


@router.get("/", response_model=list[PizzaPublicWithIngredients])
async def read_pizzas(session: SessionDep):
    pizzas = session.exec(select(Pizza)).all()
    return pizzas


@router.get("/{pizza_id}", response_model=PizzaPublicWithIngredients)
async def read_pizza(pizza_id: int, session: SessionDep):
    pizza = session.get(Pizza, pizza_id)

    if not pizza:
        raise HTTPException(status_code=404, detail="pizza not found")

    return pizza


@router.patch("/{pizza_id}", response_model=PizzaPublicWithIngredients)
async def update_pizza(pizza_update: PizzaUpdate, pizza_id: int, session: SessionDep):
    pizza = session.get(Pizza, pizza_id)

    if not pizza:
        raise HTTPException(status_code=404, detail="pizza not found")

    pizza_data = pizza_update.model_dump(exclude_unset=True)
    pizza.sqlmodel_update(pizza_data)

    session.add(pizza)
    session.commit()
    session.refresh(pizza)

    return pizza


@router.delete("/{pizza_id}")
async def delete_pizza(pizza_id: int, session: SessionDep):
    pizza = session.get(Pizza, pizza_id)

    if not pizza:
        raise HTTPException(status_code=404, detail="pizza not found")

    session.delete(pizza)
    session.commit()

    return {}
