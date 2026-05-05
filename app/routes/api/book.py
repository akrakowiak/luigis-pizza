from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlmodel import Session

from app import book
from app.cart import get_cart
from app.db import SessionDep
from app.models.restaurant_models import Reservation, Table
from app.session import get_session
from app.table import book_table as book_table_method

router = APIRouter(prefix="/book", tags=["book"])


class BookTableRequest(BaseModel):
    table_id: str
    reservation_time: datetime
    duration: timedelta


@router.get("/")
async def get_book_date(
    session: SessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
) -> book.BookingInfo | None:
    session_instance, created = get_session(session, session_id)
    if created:
        response.set_cookie(key="session_id", value=session_instance.id)

    booking_info = book.get_book_date(session, session_instance)
    return booking_info


@router.post("/")
async def book_table(
    book_table_request: BookTableRequest,
    session: SessionDep,
    response: Response,
    session_id: Annotated[str | None, Cookie()] = None,
) -> Reservation | None:
    table_id = book_table_request.table_id
    reservation_time = book_table_request.reservation_time
    duration = book_table_request.duration
    table = session.get(Table, table_id)

    if not table:
        raise HTTPException(status_code=404, detail="table not found")

    session_instance, created = get_session(session, session_id)
    if created:
        response.set_cookie(key="session_id", value=session_instance.id)

    cart = get_cart(session, session_instance.id)
    reservation = book_table_method(
        session, session_instance, table, reservation_time, duration
    )

    if not reservation:
        raise HTTPException(
            status_code=409, detail="table is already reserved at the selected time"
        )

    return reservation
