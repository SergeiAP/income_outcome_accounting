# pylint: disable=missing-module-docstring
from typing import Optional
from fastapi import APIRouter, Depends, Response, status

from ..models.operations import (
    Operation, OperationCreate, OperationKind, OperationUpdate)
from .. import tables
from ..services.operations import OperationsServices


router = APIRouter(
    prefix='/operstions'
)


@router.get('/', response_model=list[Operation])
def get_operations(kind: Optional[OperationKind] = None,
                   service: OperationsServices = Depends(),
                   ) -> list[tables.Operation]:
    """Get all operations from the db

    Args:
        kind (Optional[Operationkind], optional): filter by operation kind, if None -
        all opearions. Defaults to None.
        service (OperationsServices, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        list[tables.Operation]: all operations (filtered by `kind` or not)
    """
    return service.get_list(kind=kind)


@router.post('/', response_model=Operation)
def create_operation(operation_data: OperationCreate,
                     service: OperationsServices = Depends(),
                     ) -> tables.Operation:
    """Insert operation to database

    Args:
        operation_data (OperationCreate): operations to be inserted.
        service (OperationsServices, optional): run database session using __init__.
        Defaults to Depends().
    """
    return service.create(operation_data)


@router.get('/{operation_id}', response_model=Operation)
def get_operation(operation_id: int,
                  service: OperationsServices = Depends(),
                  ) -> tables.Operation:
    """Get operation data by id (from database)

    Args:
        operation_id (int): id of operation in database
        service (OperationsServices, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        tables.Operation: data of specific operation
    """
    return service.get(operation_id)

@router.put('/{operation_id}', response_model=Operation)
def update_operation(operation_id: int,
                     operation_data: OperationUpdate,
                     service: OperationsServices = Depends(),
                     ) -> tables.Operation:
    """Update operation by id (from database)

    Args:
        operation_id (int): operation to be updated
        operation_data (OperationUpdate): data to be updated
        service (OperationsServices, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        tables.Operation: updated data
    """
    return service.update(
        operation_id,
        operation_data
    )

@router.delete('/{operation_id}')
def delete_operation(operation_id: int,
                     service: OperationsServices = Depends(),
                     ) -> Response:
    """Delete operation by id (from database)

    Args:
        operation_id (int): _description_
        service (OperationsServices, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        Response: status code of the delection execution
    """
    service.delete(operation_id)
    # It is obligatory to have return
    return Response(status_code=status.HTTP_204_NO_CONTENT)
