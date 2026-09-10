from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_slots.id"),
        nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="CONFIRMED",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="bookings"
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="bookings"
    )

    slot = relationship(
        "ParkingSlot",
        back_populates="bookings"
    )