from datetime import datetime, timedelta

from pydantic import BaseModel
from sqlmodel import Session, select

from app.models.restaurant_models import Reservation
from app.models.restaurant_models import Session as SessionInstance


class BookingInfo(BaseModel):
    table_id: str
    reservation_time: datetime
    duration: timedelta


def get_book_date(
    session: Session, session_instance: SessionInstance
) -> BookingInfo | None:
    reservation = session.exec(
        select(Reservation).where(Reservation.session_id == session_instance.id)
    ).one_or_none()
    print(session_instance.id)
    if not reservation:
        return None

    return BookingInfo(
        table_id=reservation.table_id,
        reservation_time=reservation.from_date,
        duration=reservation.to_date - reservation.from_date,
    )
