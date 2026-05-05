from typing import Annotated

from fastapi import APIRouter, Cookie, Header, Request, Response
from sqlmodel import select

from app.cart import get_cart
from app.db import SessionDep
from app.models.pizza_ingredient import Pizza
from app.session import get_session
from app.templates import templates

router = APIRouter()


@router.get("/")
async def index(request: Request, session: SessionDep):
    pizzas = session.exec(select(Pizza)).all()

    return templates.TemplateResponse(
        "pages/main.html",
        {
            "request": request,
            "specialities": [
                {
                    "image": "./static/img/pizza/spring.jpg",
                    "name": "Pizza Wiosenna",
                    "description": """
                    Lekka pizza z rukolą i toskańskimi oliwkami, podawana z zapiekaną ricottą.
                    """,
                },
                {
                    "image": "./static/img/pizza/summer.jpg",
                    "name": "Pizza Letnia",
                    "description": """
                    Delikatna pizza z figami i prosciutto podawana na białym sosie z ocetem balsamicznym.
                    """,
                },
                {
                    "image": "./static/img/pizza/winter.jpg",
                    "name": "Pizza Zimowa",
                    "description": """
                    Obfita pizza z soczystym boczkiem, czarnymi oliwkami i amerykańskim szpinakiem Popeye'a.
                    """,
                },
            ],
        },
    )


@router.get("/menu")
async def menu(request: Request, session: SessionDep):
    pizzas = session.exec(select(Pizza)).all()

    print(f"Pobrane pizze: {pizzas}")

    return templates.TemplateResponse(
        "pages/menu.html",
        {"request": request, "pizzas": pizzas},
    )


@router.get("/summary")
async def summary(
    request: Request,
    session: SessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
):
    session_instance, created = get_session(session, session_id)
    if created:
        response.set_cookie(key="session_id", value=session_instance.id)

    cart = get_cart(session, session_instance.id)

    return templates.TemplateResponse(
        "pages/summary.html",
        {"request": request, "cart": cart},
    )


@router.get("/book")
async def book(
    request: Request,
):
    return templates.TemplateResponse(
        "pages/book.html",
        {"request": request},
    )
