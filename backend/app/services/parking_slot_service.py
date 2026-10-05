from sqlalchemy.orm import Session

from app.models.parking_slot import ParkingSlot
from app.schemas.parking_slot import (
    ParkingSlotCreate,
    ParkingSlotUpdate
)


def create_slot(db: Session, slot_data: ParkingSlotCreate):

    existing_slot = (
        db.query(ParkingSlot)
        .filter(
            ParkingSlot.slot_number == slot_data.slot_number
        )
        .first()
    )

    if existing_slot:
        return None

    slot = ParkingSlot(
        slot_number=slot_data.slot_number,
        status=slot_data.status,
        floor=slot_data.floor
    )

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return slot


def get_slots(db: Session):
    return db.query(ParkingSlot).all()


def get_slot(db: Session, slot_id: int):

    return (
        db.query(ParkingSlot)
        .filter(ParkingSlot.id == slot_id)
        .first()
    )


def update_slot(
    db: Session,
    slot_id: int,
    slot_data: ParkingSlotUpdate
):

    slot = get_slot(db, slot_id)

    if not slot:
        return None

    update_data = slot_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(slot, key, value)

    db.commit()
    db.refresh(slot)

    return slot


def delete_slot(db: Session, slot_id: int):

    slot = get_slot(db, slot_id)

    if not slot:
        return False

    db.delete(slot)
    db.commit()

    return True