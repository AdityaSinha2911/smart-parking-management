from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.parking_slot import (
    ParkingSlotCreate,
    ParkingSlotResponse,
    ParkingSlotUpdate
)
from app.services.parking_slot_service import (
    create_slot,
    delete_slot,
    get_slot,
    get_slots,
    update_slot
)


router = APIRouter(
    prefix="/parking-slots",
    tags=["Parking Slots"]
)


@router.post(
    "/",
    response_model=ParkingSlotResponse,
    status_code=status.HTTP_201_CREATED
)
def create_parking_slot(
    slot_data: ParkingSlotCreate,
    db: Session = Depends(get_db)
):

    slot = create_slot(db, slot_data)

    if not slot:
        raise HTTPException(
            status_code=400,
            detail="Slot number already exists"
        )

    return slot


@router.get(
    "/",
    response_model=list[ParkingSlotResponse]
)
def read_parking_slots(
    db: Session = Depends(get_db)
):

    return get_slots(db)


@router.get(
    "/{slot_id}",
    response_model=ParkingSlotResponse
)
def read_parking_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):

    slot = get_slot(db, slot_id)

    if not slot:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return slot


@router.put(
    "/{slot_id}",
    response_model=ParkingSlotResponse
)
def update_parking_slot(
    slot_id: int,
    slot_data: ParkingSlotUpdate,
    db: Session = Depends(get_db)
):

    slot = update_slot(
        db,
        slot_id,
        slot_data
    )

    if not slot:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return slot


@router.delete(
    "/{slot_id}"
)
def delete_parking_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_slot(db, slot_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return {
        "message": "Parking slot deleted successfully"
    }