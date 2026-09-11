from sqlalchemy.orm import Session

from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate


def create_vehicle(db: Session, vehicle_data: VehicleCreate):

    user = (
        db.query(User)
        .filter(User.id == vehicle_data.user_id)
        .first()
    )

    if not user:
        return None, "user_not_found"

    existing_vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.vehicle_number == vehicle_data.vehicle_number
        )
        .first()
    )

    if existing_vehicle:
        return None, "vehicle_exists"

    vehicle = Vehicle(
        user_id=vehicle_data.user_id,
        vehicle_number=vehicle_data.vehicle_number,
        vehicle_type=vehicle_data.vehicle_type
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle, None


def get_vehicles(db: Session):
    return db.query(Vehicle).all()


def get_vehicle(db: Session, vehicle_id: int):

    return (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id)
        .first()
    )


def update_vehicle(
    db: Session,
    vehicle_id: int,
    vehicle_data: VehicleUpdate
):

    vehicle = get_vehicle(db, vehicle_id)

    if not vehicle:
        return None

    update_data = vehicle_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(vehicle, key, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


def delete_vehicle(db: Session, vehicle_id: int):

    vehicle = get_vehicle(db, vehicle_id)

    if not vehicle:
        return False

    db.delete(vehicle)
    db.commit()

    return True