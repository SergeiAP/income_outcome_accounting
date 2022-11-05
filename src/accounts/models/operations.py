# pylint: disable=missing-module-docstring
from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional
from pydantic import BaseModel


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
