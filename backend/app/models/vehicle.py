from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

# Vehicle model representing a vehicle in the system, with attributes for vehicle number, type, and relationships to users and bookings.
class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    vehicle_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    vehicle_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="vehicles"
    )

    bookings = relationship(
        "Booking",
        back_populates="vehicle"
    )