from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import SessionDep
from app.models.restaurant_models import Reservation, Table

router = APIRouter(prefix="/table", tags=["table"])


class TableInfo(BaseModel):
    reservation_time: datetime
    duration: timedelta


@router.get("/{table_id}")
async def check_table_availability(
    table_id: str, session: SessionDep
) -> Reservation | None:
    table = session.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="table not found")

    reservation = session.exec(
        select(Reservation)
        .where(Reservation.table == table, Reservation.to_date > datetime.now())
        .order_by(Reservation.from_date)
    ).first()
    return reservation
