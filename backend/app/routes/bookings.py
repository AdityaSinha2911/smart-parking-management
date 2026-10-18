from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import get_current_user
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.services.booking_service import create_booking, get_bookings, get_booking, update_booking, delete_booking

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
def create_new_booking(booking_data: BookingCreate, db: Session = Depends(get_db)):
    booking, error = create_booking(db, booking_data)
    errors = {
        "user_not_found": (404, "User not found"),
        "vehicle_not_found": (404, "Vehicle not found"),
        "slot_not_found": (404, "Parking slot not found"),
        "slot_unavailable": (400, "Parking slot is not available"),
        "invalid_time": (400, "Start time must be before end time"),
    }
    if error in errors:
        code, detail = errors[error]
        raise HTTPException(status_code=code, detail=detail)
    return booking


@router.get("/me", response_model=list[BookingResponse])
def read_current_user_bookings(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return [booking for booking in get_bookings(db) if booking.user_id == user_id]


@router.get("/", response_model=list[BookingResponse], dependencies=[Depends(get_current_user)])
def read_bookings(db: Session = Depends(get_db)):
    return get_bookings(db)


@router.get("/{booking_id}", response_model=BookingResponse, dependencies=[Depends(get_current_user)])
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.put("/{booking_id}", response_model=BookingResponse, dependencies=[Depends(get_current_user)])
def update_existing_booking(booking_id: int, booking_data: BookingUpdate, db: Session = Depends(get_db)):
    booking = update_booking(db, booking_id, booking_data)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.delete("/{booking_id}", dependencies=[Depends(get_current_user)])
def delete_existing_booking(booking_id: int, db: Session = Depends(get_db)):
    deleted = delete_booking(db, booking_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted successfully"}
