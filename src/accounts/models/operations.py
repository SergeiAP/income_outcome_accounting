# pylint: disable=missing-module-docstring
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel, root_validator  # pylint: disable=no-name-in-module


class OperationKind(str, Enum):
    """Fixed kind of operations"""
    INCOME = 'income'
    OUTCOME = 'outcome'


class OperationBase(BaseModel):
    """Base class for operation table manipulations"""
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]


class Operation(OperationBase):
    """Schema of operation table in db"""
    id: int

    class Config:
        """Upload from ORM"""
        orm_mode = True


class OperationCreate(OperationBase):
    """Schema to create a new operation"""


class OperationUpdate(OperationBase):
    """Schema to update operation"""


class OperationsNumChange(BaseModel):
    """Schema to show chnaged number of rows"""
    rows_number_before: int
    rows_number_after: int

    @root_validator(pre=False)
    def calculate_number_diff(cls, values) -> dict:  # pylint: disable=no-self-argument
        """Calculate roews differewnce"""
        values["rows_number_difference"] = (
            values.get("rows_number_after") - values.get("rows_number_before"))
        return values
