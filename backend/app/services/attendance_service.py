from typing import List
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.models.attendance import Attendance, AttendanceCreate, AttendanceResponse
from app.services.employee_service import employee_service
from app.utils.exceptions import EmployeeNotFoundError


class AttendanceService:
    """Service for attendance management operations."""
    
    async def mark_attendance(self, db: AsyncSession, attendance: AttendanceCreate) -> AttendanceResponse:
        """
        Mark or update attendance for an employee.
        
        If attendance already exists for the given date, it will be updated.
        Otherwise, a new attendance record will be created.
        
        Args:
            db: Database session
            attendance: Attendance data
            
        Returns:
            Created or updated attendance record
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
        """
        # Verify employee exists
        employee = await employee_service.get_employee_by_id(db, attendance.employee_id)
        if not employee:
            raise EmployeeNotFoundError(attendance.employee_id)
        
        # Check if attendance already exists for this date
        stmt = select(Attendance).where(
            and_(
                Attendance.employee_id == attendance.employee_id,
                Attendance.date == attendance.date
            )
        )
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing attendance
            existing.status = attendance.status
            await db.commit()
            await db.refresh(existing)
            return AttendanceResponse.model_validate(existing)
        
        # Create new attendance record
        db_attendance = Attendance(
            id=f"att_{uuid.uuid4().hex[:12]}",
            employee_id=attendance.employee_id,
            date=attendance.date,
            status=attendance.status
        )
        db.add(db_attendance)
        await db.commit()
        await db.refresh(db_attendance)
        
        return AttendanceResponse.model_validate(db_attendance)
    
    async def get_employee_attendance(self, db: AsyncSession, employee_id: str) -> List[AttendanceResponse]:
        """
        Get all attendance records for a specific employee.
        
        Args:
            db: Database session
            employee_id: Employee ID
            
        Returns:
            List of attendance records ordered by date (newest first)
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
        """
        # Verify employee exists
        employee = await employee_service.get_employee_by_id(db, employee_id)
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        
        stmt = select(Attendance).where(
            Attendance.employee_id == employee_id
        ).order_by(Attendance.date.desc())
        
        result = await db.execute(stmt)
        records = result.scalars().all()
        
        return [AttendanceResponse.model_validate(record) for record in records]
    
    async def get_attendance_by_date(self, db: AsyncSession, attendance_date: date) -> List[AttendanceResponse]:
        """
        Get all attendance records for a specific date.
        
        Args:
            db: Database session
            attendance_date: Date to filter by
            
        Returns:
            List of attendance records for the specified date
        """
        stmt = select(Attendance).where(Attendance.date == attendance_date)
        result = await db.execute(stmt)
        records = result.scalars().all()
        
        return [AttendanceResponse.model_validate(record) for record in records]
    
    async def get_all_attendance(self, db: AsyncSession) -> List[AttendanceResponse]:
        """
        Get all attendance records.
        
        Args:
            db: Database session
            
        Returns:
            List of all attendance records ordered by date (newest first)
        """
        stmt = select(Attendance).order_by(Attendance.date.desc())
        result = await db.execute(stmt)
        records = result.scalars().all()
        
        return [AttendanceResponse.model_validate(record) for record in records]


# Singleton instance
attendance_service = AttendanceService()
