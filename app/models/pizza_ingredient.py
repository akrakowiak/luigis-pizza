import enum
from decimal import Decimal
from typing import Annotated

from pydantic import PlainValidator, WrapSerializer
from sqlmodel import (
    Field,
    ForeignKeyConstraint,
    Numeric,
    Relationship,
    SQLModel,
    String,
)


class PizzaSize(enum.Enum):
    small = 1
    medium = 2
    large = 3


class PizzaIngredientLink(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(
            ["pizza_id"], ["pizza.id"], use_alter=True, ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ["ingredient_id"], ["ingredient.id"], use_alter=True, ondelete="CASCADE"
        ),
    )
    pizza_id: str = Field(sa_type=String(32), primary_key=True)
    ingredient_id: str = Field(sa_type=String(32), primary_key=True)


class PizzaBase(SQLModel):
    name: str | None = Field(index=True)
    description: str | None = Field()
    small_price: Decimal = Field(sa_type=Numeric(5, 2))
    medium_price: Decimal = Field(sa_type=Numeric(5, 2))
    large_price: Decimal = Field(sa_type=Numeric(5, 2))
    spiciness: int
    vegetarian: bool


class Pizza(PizzaBase, table=True):
    id: str = Field(sa_type=String(32), primary_key=True)
    ingredients: list["Ingredient"] = Relationship(
        back_populates="pizzas", link_model=PizzaIngredientLink
    )


class PizzaPublic(PizzaBase):
    id: str = Field()


class PizzaPublicWithIngredients(PizzaPublic):
    ingredients: list["Ingredient"] = []


class PizzaPublicWithSize(PizzaPublic):
    size: PizzaSize


class PizzaCreate(PizzaBase):
    pass


class PizzaUpdate(PizzaBase):
    name: str | None = None


class IngredientBase(SQLModel):
    name: str = Field(index=True)


class Ingredient(IngredientBase, table=True):
    id: str = Field(sa_type=String(32), primary_key=True)
    pizzas: list["Pizza"] = Relationship(
        back_populates="ingredients", link_model=PizzaIngredientLink
    )


class IngredientPublic(IngredientBase):
    id: str


class IngredientPublicWithPizzas(IngredientPublic):
    pizzas: list["Pizza"] = []
