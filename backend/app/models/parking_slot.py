from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
# Represents a parking slot in the parking management system
class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id: Mapped[int] = mapped_column(primary_key=True)

    slot_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="AVAILABLE",
        nullable=False
    )

    floor: Mapped[int] = mapped_column(
        nullable=False
    )

    bookings = relationship(
        "Booking",
        back_populates="slot"
    )