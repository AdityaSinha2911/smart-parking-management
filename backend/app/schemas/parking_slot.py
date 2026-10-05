from pydantic import BaseModel, ConfigDict


class ParkingSlotCreate(BaseModel):
    slot_number: str
    status: str = "AVAILABLE"
    floor: int


class ParkingSlotUpdate(BaseModel):
    slot_number: str | None = None
    status: str | None = None
    floor: int | None = None


class ParkingSlotResponse(BaseModel):
    id: int
    slot_number: str
    status: str
    floor: int

    model_config = ConfigDict(from_attributes=True)