from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attendance import AttendanceCreate, AttendanceResponse
from app.services.attendance_service import attendance_service
from app.utils.exceptions import EmployeeNotFoundError, InvalidAttendanceError
from app.database import get_db

router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])


@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mark attendance for an employee"
)
async def mark_attendance(
    attendance: AttendanceCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Mark attendance for an employee:
    - **employee_id**: Employee identifier
    - **date**: Attendance date (YYYY-MM-DD format)
    - **status**: Either "Present" or "Absent"
    
    If attendance already exists for the given date, it will be updated.
    """
    try:
        return await attendance_service.mark_attendance(db, attendance)
    except EmployeeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except InvalidAttendanceError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.get(
    "/employee/{employee_id}",
    response_model=List[AttendanceResponse],
    summary="Get attendance records for an employee"
)
async def get_employee_attendance(
    employee_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all attendance records for a specific employee.
    Records are sorted by date in descending order (most recent first).
    """
    try:
        return await attendance_service.get_employee_attendance(db, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.get(
    "",
    response_model=List[AttendanceResponse],
    summary="Get all attendance records or filter by date"
)
async def get_attendance(
    attendance_date: Optional[date] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get attendance records:
    - Without date parameter: Returns all attendance records
    - With date parameter: Returns attendance for specific date (bonus feature)
    """
    if attendance_date:
        return await attendance_service.get_attendance_by_date(db, attendance_date)
    else:
        return await attendance_service.get_all_attendance(db)
