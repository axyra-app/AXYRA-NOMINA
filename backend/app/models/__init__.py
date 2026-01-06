"""
Modelos de la aplicación
"""

from app.models.employee import (
    EmployeeBase,
    EmployeeCreate,
    EmployeeUpdate,
    Employee,
)

from app.models.hours import (
    HoursBase,
    HoursCreate,
    HoursUpdate,
    Hours,
)

from app.models.payroll import (
    PayrollDetailItem,
    PayrollSummary,
    PayrollCalculation,
    PayrollBatch,
)

from app.models.configuration import (
    CompanyConfig,
    HourTypeConfig,
    HourConfiguration,
    ConfigurationUpdate,
    SystemSettings,
)

__all__ = [
    # Employee
    "EmployeeBase",
    "EmployeeCreate",
    "EmployeeUpdate",
    "Employee",
    # Hours
    "HoursBase",
    "HoursCreate",
    "HoursUpdate",
    "Hours",
    # Payroll
    "PayrollDetailItem",
    "PayrollSummary",
    "PayrollCalculation",
    "PayrollBatch",
    # Configuration
    "CompanyConfig",
    "HourTypeConfig",
    "HourConfiguration",
    "ConfigurationUpdate",
    "SystemSettings",
]
