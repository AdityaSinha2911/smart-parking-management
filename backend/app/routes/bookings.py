from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse
)

from app.services.booking_service import (
    create_booking,
    get_bookings,
    get_booking,
    update_booking,
    delete_booking
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):

    booking, error = create_booking(
        db,
        booking_data
    )

    if error == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if error == "vehicle_not_found":
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    if error == "slot_not_found":
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    if error == "slot_unavailable":
        raise HTTPException(
            status_code=400,
            detail="Parking slot is not available"
        )

    if error == "invalid_time":
        raise HTTPException(
            status_code=400,
            detail="Start time must be before end time"
        )

    return booking


@router.get(
    "/",
    response_model=list[BookingResponse]
)
def read_bookings(
    db: Session = Depends(get_db)
):

    return get_bookings(db)


@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = get_booking(
        db,
        booking_id
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@router.put(
    "/{booking_id}",
    response_model=BookingResponse
)
def update_existing_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db)
):

    booking = update_booking(
        db,
        booking_id,
        booking_data
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@router.delete("/{booking_id}")
def delete_existing_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_booking(
        db,
        booking_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return {
        "message": "Booking deleted successfully"
    }