from pydantic import BaseModel, ConfigDict


class VehicleCreate(BaseModel):
    user_id: int
    vehicle_number: str
    vehicle_type: str


class VehicleUpdate(BaseModel):
    vehicle_number: str | None = None
    vehicle_type: str | None = None


class VehicleResponse(BaseModel):
    id: int
    user_id: int
    vehicle_number: str
    vehicle_type: str

    model_config = ConfigDict(from_attributes=True)