from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    user_id: int
    vehicle_id: int
    slot_id: int
    start_time: datetime
    end_time: datetime


class BookingUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str | None = None


class BookingResponse(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    slot_id: int
    start_time: datetime
    end_time: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)