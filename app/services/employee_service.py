from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.employee import Employee, EmployeeCreate, EmployeeResponse
from app.models.attendance import Attendance
from app.utils.exceptions import EmployeeNotFoundError, DuplicateEmployeeError


class EmployeeService:
    """Service for employee CRUD operations."""
    
    async def create_employee(self, db: AsyncSession, employee: EmployeeCreate) -> EmployeeResponse:
        """
        Create a new employee with auto-generated sequential ID.
        Employee IDs are generated in format: EMP001, EMP002, EMP003, etc.
        
        Args:
            db: Database session
            employee: Employee data to create
            
        Returns:
            Created employee with auto-generated employee_id
            
        Raises:
            DuplicateEmployeeError: If email already exists
        """
        try:
            # Count existing employees to generate next sequential ID
            count_query = select(func.count()).select_from(Employee)
            result = await db.execute(count_query)
            employee_count = result.scalar()
            
            # Generate sequential employee_id: EMP001, EMP002, etc.
            employee_id = f"EMP{employee_count + 1:03d}"
            
            db_employee = Employee(
                employee_id=employee_id,
                full_name=employee.full_name,
                email=employee.email,
                department=employee.department
            )
            
            db.add(db_employee)
            await db.commit()
            await db.refresh(db_employee)
            
            return EmployeeResponse.model_validate(db_employee)
            
        except IntegrityError as e:
            await db.rollback()
            error_msg = str(e).lower()
            
            if "email" in error_msg:
                raise DuplicateEmployeeError(f"Email {employee.email} already exists")
            raise
    
    async def get_all_employees(self, db: AsyncSession) -> List[EmployeeResponse]:
        """
        Get all employees ordered by creation date (newest first).
        
        Args:
            db: Database session
            
        Returns:
            List of all employees
        """
        stmt = select(Employee).order_by(Employee.created_at.desc())
        result = await db.execute(stmt)
        employees = result.scalars().all()
        
        return [EmployeeResponse.model_validate(emp) for emp in employees]
    
    async def get_employee_by_id(self, db: AsyncSession, employee_id: str) -> Optional[EmployeeResponse]:
        """
        Get employee by employee_id.
        
        Args:
            db: Database session
            employee_id: Employee ID to search for
            
        Returns:
            Employee if found, None otherwise
        """
        stmt = select(Employee).where(Employee.employee_id == employee_id)
        result = await db.execute(stmt)
        employee = result.scalar_one_or_none()
        
        return EmployeeResponse.model_validate(employee) if employee else None
    
    async def delete_employee(self, db: AsyncSession, employee_id: str) -> bool:
        """
        Delete employee and cascade delete their attendance records.
        
        Args:
            db: Database session
            employee_id: Employee ID to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            EmployeeNotFoundError: If employee doesn't exist
        """
        stmt = select(Employee).where(Employee.employee_id == employee_id)
        result = await db.execute(stmt)
        employee = result.scalar_one_or_none()
        
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        
        # Delete attendance records (CASCADE will handle this, but being explicit)
        await db.execute(
            delete(Attendance).where(Attendance.employee_id == employee_id)
        )
        
        # Delete employee
        await db.delete(employee)
        await db.commit()
        
        return True


# Singleton instance
employee_service = EmployeeService()
