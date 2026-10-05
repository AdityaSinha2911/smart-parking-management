from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.parking_slot import ParkingSlot

from app.schemas.booking import BookingCreate, BookingUpdate


def create_booking(db: Session, booking_data: BookingCreate):

    # Check user
    user = (
        db.query(User)
        .filter(User.id == booking_data.user_id)
        .first()
    )

    if not user:
        return None, "user_not_found"


    # Check vehicle
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == booking_data.vehicle_id)
        .first()
    )

    if not vehicle:
        return None, "vehicle_not_found"


    # Check parking slot
    slot = (
        db.query(ParkingSlot)
        .filter(ParkingSlot.id == booking_data.slot_id)
        .first()
    )

    if not slot:
        return None, "slot_not_found"


    # Check slot availability
    if slot.status != "AVAILABLE":
        return None, "slot_unavailable"


    # Check time validity
    if booking_data.start_time >= booking_data.end_time:
        return None, "invalid_time"


    # Create booking
    booking = Booking(
        user_id=booking_data.user_id,
        vehicle_id=booking_data.vehicle_id,
        slot_id=booking_data.slot_id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        status="CONFIRMED"
    )

    db.add(booking)

    # Mark slot occupied
    slot.status = "OCCUPIED"

    db.commit()
    db.refresh(booking)

    return booking, None


def get_bookings(db: Session):
    return db.query(Booking).all()


def get_booking(db: Session, booking_id: int):

    return (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )


def update_booking(
    db: Session,
    booking_id: int,
    booking_data: BookingUpdate
):

    booking = get_booking(db, booking_id)

    if not booking:
        return None

    update_data = booking_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)

    return booking


def delete_booking(db: Session, booking_id: int):

    booking = get_booking(db, booking_id)

    if not booking:
        return False

    # Free the parking slot
    slot = (
        db.query(ParkingSlot)
        .filter(ParkingSlot.id == booking.slot_id)
        .first()
    )

    if slot:
        slot.status = "AVAILABLE"

    db.delete(booking)

    db.commit()

    return True