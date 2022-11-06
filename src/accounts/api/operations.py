# pylint: disable=missing-module-docstring
from typing import Optional
from fastapi import APIRouter, Depends, Response, status

from ..models.auth import User
from ..services.auth import get_current_user
from ..models.operations import (
    Operation, OperationCreate, OperationKind, OperationUpdate)
from .. import tables
from ..services.operations import OperationsService


router = APIRouter(
    prefix='/operations',
    tags=['operations'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/', response_model=list[Operation])
def get_operations(kind: Optional[OperationKind] = None,
                   user: User = Depends(get_current_user),
                   service: OperationsService = Depends(),
                   ) -> list[tables.Operation]:
    """Get all operations from the db

    Args:
        kind (Optional[Operationkind], optional): filter by operation kind, if None -
        all opearions. Defaults to None.
        user (User, optional): authentificated user with it's data.
        Defaults to Depends(get_current_user).
        service (OperationsService, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        list[tables.Operation]: all operations (filtered by `kind` or not)
    """
    return service.get_list(user_id=user.id, kind=kind)


@router.post('/', response_model=Operation)
def create_operation(operation_data: OperationCreate,
                     user: User = Depends(get_current_user),
                     service: OperationsService = Depends(),
                     ) -> tables.Operation:
    """Insert operation to database

    Args:
        operation_data (OperationCreate): operations to be inserted.
        user (User, optional): authentificated user with it's data.
        Defaults to Depends(get_current_user).
        service (OperationsService, optional): run database session using __init__.
        Defaults to Depends().
    """
    return service.create(user_id=user.id, operation_data=operation_data)


@router.get('/{operation_id}', response_model=Operation)
def get_operation(operation_id: int,
                  user: User = Depends(get_current_user),
                  service: OperationsService = Depends(),
                  ) -> tables.Operation:
    """Get operation data by id (from database)

    Args:
        operation_id (int): id of operation in database
        user (User, optional): authentificated user with it's data.
        Defaults to Depends(get_current_user).
        service (OperationsService, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        tables.Operation: data of specific operation
    """
    return service.get(user_id=user.id, operation_id=operation_id)

@router.put('/{operation_id}', response_model=Operation)
def update_operation(operation_id: int,
                     operation_data: OperationUpdate,
                     user: User = Depends(get_current_user),
                     service: OperationsService = Depends(),
                     ) -> tables.Operation:
    """Update operation by id (from database)

    Args:
        operation_id (int): operation to be updated
        operation_data (OperationUpdate): data to be updated
        user (User, optional): authentificated user with it's data.
        Defaults to Depends(get_current_user).
        service (OperationsService, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        tables.Operation: updated data
    """
    return service.update(
        user_id=user.id,
        operation_id=operation_id,
        operation_data=operation_data,
    )

@router.delete('/{operation_id}')
def delete_operation(operation_id: int,
                     user: User = Depends(get_current_user),
                     service: OperationsService = Depends(),
                     ) -> Response:
    """Delete operation by id (from database)

    Args:
        operation_id (int): operation to be deleted
        user (User, optional): authentificated user with it's data.
        Defaults to Depends(get_current_user).
        service (OperationsService, optional): run database session using __init__.
        Defaults to Depends().

    Returns:
        Response: status code of the delection execution
    """
    service.delete(user_id=user.id, operation_id=operation_id)
    # It is obligatory to have return
    return Response(status_code=status.HTTP_204_NO_CONTENT)
