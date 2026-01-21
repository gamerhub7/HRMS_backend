from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import EmployeeCreate, EmployeeResponse
from app.services.employee_service import employee_service
from app.utils.exceptions import EmployeeNotFoundError, DuplicateEmployeeError
from app.database import get_db

router = APIRouter(prefix="/api/v1/employees", tags=["employees"])


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee"
)
async def create_employee(
    employee: EmployeeCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new employee with the following information:
    - **employee_id**: Unique employee identifier
    - **full_name**: Employee's full name
    - **email**: Valid email address
    - **department**: Department name
    """
    try:
        return await employee_service.create_employee(db, employee)
    except DuplicateEmployeeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.get(
    "",
    response_model=List[EmployeeResponse],
    summary="Get all employees"
)
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all employees in the system.
    Returns an empty list if no employees exist.
    """
    return await employee_service.get_all_employees(db)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID"
)
async def get_employee(
    employee_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific employee by their employee_id.
    """
    employee = await employee_service.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an employee"
)
async def delete_employee(
    employee_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an employee and all their attendance records.
    This action cannot be undone.
    """
    try:
        await employee_service.delete_employee(db, employee_id)
    except EmployeeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
