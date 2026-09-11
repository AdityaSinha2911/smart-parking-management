from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate
)
from app.services.vehicle_service import (
    create_vehicle,
    delete_vehicle,
    get_vehicle,
    get_vehicles,
    update_vehicle
)


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
):

    vehicle, error = create_vehicle(
        db,
        vehicle_data
    )

    if error == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if error == "vehicle_exists":
        raise HTTPException(
            status_code=400,
            detail="Vehicle number already registered"
        )

    return vehicle


@router.get(
    "/",
    response_model=list[VehicleResponse]
)
def read_vehicles(
    db: Session = Depends(get_db)
):

    return get_vehicles(db)


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def read_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    vehicle = get_vehicle(
        db,
        vehicle_id
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def update_existing_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):

    vehicle = update_vehicle(
        db,
        vehicle_id,
        vehicle_data
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return vehicle


@router.delete(
    "/{vehicle_id}"
)
def delete_existing_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_vehicle(
        db,
        vehicle_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found"
        )

    return {
        "message": "Vehicle deleted successfully"
    }