from sqlalchemy import Column, String, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from app.database import Base


# SQLAlchemy Model
class Attendance(Base):
    """Attendance database model."""
    __tablename__ = "attendance"
    
    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(10), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("status IN ('Present', 'Absent')", name='check_status'),
    )


# Pydantic Models
class AttendanceBase(BaseModel):
    """Base attendance model with core fields."""
    employee_id: str
    date: date
    status: str  # "Present" or "Absent"


class AttendanceCreate(AttendanceBase):
    """Model for creating attendance records."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "employee_id": "EMP001",
                "date": "2024-01-21",
                "status": "Present"
            }
        }
    )


class AttendanceResponse(AttendanceBase):
    """Model for attendance API responses."""
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
