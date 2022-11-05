# pylint: disable=missing-module-docstring
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models.operations import OperationCreate, OperationKind, OperationUpdate

from .. import tables
from ..database import get_session


class OperationsServices:
    """Class to store operations business logic"""
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, operation_id: int) -> tables.Operation:
        """Get specific operation by id

        Args:
            operation_id (int): operation id

        Raises:
            HTTPException: if there is no operation with such id

        Returns:
            tables.Operation: data of specific operation
        """
        operation = (
            self.session
            .query(tables.Operation)
            .filter_by(id=operation_id)
            .first()
        )
        if not operation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, kind: Optional[OperationKind] = None) -> list[tables.Operation]:
        """Return all operations

        Returns:
            kind (Optional[Operationkind], optional): filter by operation kind or not.
            Defaults to None.
            list[tables.Operation]: operations
        """
        query = self.session.query(tables.Operation)
        if kind:
            query = query.filter_by(kind=kind)
        operations = query.all()
        return operations

    def get(self, operation_id: int) -> tables.Operation:
        """Get specific operation by id

        Args:
            operation_id (int): operation id

        Raises:
            HTTPException: if there is no operation with such id

        Returns:
            tables.Operation: data of specific operation
        """
        return self._get(operation_id)

    def create(self, operation_data: OperationCreate) -> tables.Operation:
        """Insert operations to database

        Args:
            operation_data (OperationCreate): data to be inserted into `operation`
            table

        Returns:
            tables.Operation: return operation_data with id
        """
        operation = tables.Operation(**operation_data.dict(),)
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self,
               operation_id: int,
               operation_data: OperationUpdate
               ) -> tables.Operation:
        """Update operation by operation_id or raise 403

        Args:
            operation_id (int): opeartion to update (id from database)
            operation_data (OperationUpdate): data to update

        Returns:
            tables.Operation: updated operation
        """
        operation = self._get(operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(self, operation_id: int) -> None:
        """Delete specific operation by id or raise 403

        Args:
            operation_id (int): opeartion to delete (id from database)
        """
        operation = self._get(operation_id)
        self.session.delete(operation)
        self.session.commit()
