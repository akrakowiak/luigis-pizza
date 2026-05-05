import uuid
from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.models.restaurant_models import Reservation, Table
from app.models.restaurant_models import Session as SessionInstance


def book_table(
    session: Session,
    session_instance: SessionInstance,
    table: Table,
    reservation_time: datetime,
    duration: timedelta,
):
    conflicting_reservation = session.exec(
        select(Reservation).where(
            Reservation.table_id == table.id,
            Reservation.from_date < reservation_time + duration,
            Reservation.to_date > reservation_time,
        )
    ).all()

    if conflicting_reservation:
        return None

    reservation = Reservation(
        from_date=reservation_time,
        to_date=reservation_time + duration,
        session=session_instance,
        table=table,
    )
    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation
