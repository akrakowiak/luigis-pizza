import uuid
from http import cookies
from typing import Annotated

from fastapi import Cookie, Request, Response
from sqlmodel import Session

from app.models.restaurant_models import Cart, Session


def create_session(session: Session) -> tuple[Session, Annotated[bool, "created"]]:
    session_obj = Session()
    cart = Cart()

    session_obj.cart = cart
    cart.session_id = session_obj.id

    session.add(session_obj)
    session.add(cart)

    session.commit()
    session.refresh(session_obj)
    session.refresh(cart)

    return (session_obj, True)


def get_session(
    session: Session, session_id: str | None
) -> tuple[Session, Annotated[bool, "created"]]:
    if session_id is None:
        session_created = create_session(session)
        return session_created

    session_obj = session.get(Session, session_id)

    if not session_obj:
        session_created = create_session(session)
        return session_created

    return (session_obj, False)
