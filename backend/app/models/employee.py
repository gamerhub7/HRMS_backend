from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.database import Base


# SQLAlchemy Model
class Employee(Base):
    """Employee database model."""
    __tablename__ = "employees"
    
    employee_id = Column(String(50), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    department = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Pydantic Models
class EmployeeBase(BaseModel):
    """Base employee model with core fields."""
    full_name: str
    email: EmailStr
    department: str


class EmployeeCreate(EmployeeBase):
    """Model for creating a new employee. Employee ID is auto-generated."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@company.com",
                "department": "Engineering"
            }
        }
    )


class EmployeeResponse(EmployeeBase):
    """Model for employee API responses."""
    employee_id: str  # Auto-generated in format: EMP001, EMP002, etc.
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
