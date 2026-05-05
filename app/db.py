from typing import Annotated, Any, TypeVar

import yaml
from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import InstrumentedAttribute
from sqlmodel import Session, SQLModel, create_engine, select

from app.main import settings
from app.models.pizza_ingredient import Ingredient, Pizza
from app.models.restaurant_models import Cart, Table

engine = create_engine(settings.DATABASE_URL)


T = TypeVar("T")


def add_if_missing(session: Session, new_item: Any, attribute: InstrumentedAttribute):
    class_ = attribute.class_
    key = attribute.key
    found_items = session.exec(
        select(class_).where(attribute == getattr(new_item, key))
    )

    assert class_ is type(new_item), "attribute's class doesn't match new_item's class"

    try:
        found_item = found_items.one()
        return found_item
    except (NoResultFound, MultipleResultsFound):
        session.exec(delete(class_).where(attribute == getattr(new_item, key)))  # type: ignore
        session.commit()
        session.add(new_item)


assert isinstance(Pizza.name, InstrumentedAttribute)


def add_ingredients(session: Session):
    with open("app/data/ingredients.yaml", "r") as f:
        f_yaml = yaml.safe_load(f)
        ingredients_yaml = f_yaml["ingredients"]

        for ing_id, ing_yaml in ingredients_yaml.items():
            ing = Ingredient(id=ing_id, name=ing_yaml["name"])
            add_if_missing(session, ing, Ingredient.name)

        session.commit()


def add_pizzas(session: Session):
    with open("app/data/pizzas.yaml", "r") as f:
        f_yaml = yaml.safe_load(f)
        pizzas_yaml = f_yaml["pizzas"]

        for pizza_id, pizza_yaml in pizzas_yaml.items():
            ingredient_names = pizza_yaml["ingredients"]
            ingredients = session.exec(
                select(Ingredient).where(Ingredient.name.in_(ingredient_names))
            ).all()

            pizza = Pizza(
                id=pizza_id,
                name=pizza_yaml["name"],
                summary=pizza_yaml["summary"],
                description=pizza_yaml["description"],
                ingredients=ingredients,
                small_price=pizza_yaml["price"]["small"],
                medium_price=pizza_yaml["price"]["medium"],
                large_price=pizza_yaml["price"]["large"],
                spiciness=pizza_yaml["spiciness"],
                vegetarian=pizza_yaml["vegetarian"],
            )
            add_if_missing(session, pizza, Pizza.name)

        session.commit()


def add_tables(session: Session):
    with open("app/data/tables.yaml", "r") as f:
        f_yaml = yaml.safe_load(f)
        tables_yaml = f_yaml["tables"]

        for table_id, table_yaml in tables_yaml.items():
            table = Table(
                id=table_id,
                capacity=table_yaml["capacity"],
            )
            add_if_missing(session, table, Table.id)

        session.commit()


def add_example_data() -> None:
    with Session(engine) as session:
        add_ingredients(session)
        add_pizzas(session)
        add_tables(session)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
