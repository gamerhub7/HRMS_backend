"""Custom exceptions for HRMS Lite API."""


class HRMSException(Exception):
    """Base exception for HRMS Lite."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EmployeeNotFoundError(HRMSException):
    """Raised when employee is not found."""
    def __init__(self, employee_id: str):
        super().__init__(f"Employee with ID '{employee_id}' not found")


class DuplicateEmployeeError(HRMSException):
    """Raised when trying to create duplicate employee."""
    def __init__(self, identifier: str):
        super().__init__(f"Employee with identifier '{identifier}' already exists")


class InvalidAttendanceError(HRMSException):
    """Raised when attendance data is invalid."""
    pass
