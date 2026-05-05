import enum
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.dialects import postgresql
from sqlmodel import (
    Enum,
    Field,
    Relationship,
    SQLModel,
)

from app.models.pizza_ingredient import Pizza, PizzaSize


class Table(SQLModel, table=True):
    id: str = Field(primary_key=True)
    capacity: int = Field(nullable=False)


class Reservation(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, sa_type=postgresql.UUID
    )
    from_date: datetime = Field(nullable=False)
    to_date: datetime = Field(nullable=False)

    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: "Session" = Relationship(back_populates="reservation")

    table_id: str = Field(foreign_key="table.id")
    table: Table = Relationship()


class Cart(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, sa_type=postgresql.UUID
    )
    order_date: datetime | None

    session_id: uuid.UUID = Field(foreign_key="session.id")
    session: "Session" = Relationship(back_populates="cart")

    cart_pizzas: List["CartPizza"] = Relationship(back_populates="cart")


class CartPizza(SQLModel, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, sa_type=postgresql.UUID
    )

    cart_id: uuid.UUID = Field(foreign_key="cart.id", sa_type=postgresql.UUID)
    cart: Cart = Relationship(back_populates="cart_pizzas")

    pizza_id: str = Field(foreign_key="pizza.id")
    pizza: Pizza = Relationship()
    pizza_size: PizzaSize


class SessionBase(SQLModel):
    pass


class Session(SessionBase, table=True):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, sa_type=postgresql.UUID
    )
    cart: Cart = Relationship(back_populates="session")
    reservation: Reservation = Relationship(back_populates="session")
