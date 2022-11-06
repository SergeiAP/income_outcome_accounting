# pylint: disable=missing-module-docstring
import os
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse

from ..models.operations import OperationsNumChange

from ..models.auth import User
from ..services.auth import get_current_user
from ..services.reports import ReportsService


router = APIRouter(
    prefix='/reports',
    tags=['reports'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/export')
def export_csv(user: User = Depends(get_current_user),
               reports_service: ReportsService = Depends(),
               ) -> StreamingResponse:
    """Export operations data of specific user

    Args:
        user (User, optional): authentificated user with it's data. Defaults to
        Depends(get_current_user).
        reports_service (ReportsService, optional): service to export csv from database
        . Defaults to Depends().

    Returns:
        StreamingResponse: file as attachments in async mode
    """
    file = reports_service.export_csv(user.id)
    # StreamingResponse async send file to the client
    return StreamingResponse(
        file,
        media_type='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=report_userid{user.id}.csv'
        }
    )


@router.post('/import')
def import_csv(background_tasks: BackgroundTasks,
               file: UploadFile = File(...),  # also exists async method
               user: User = Depends(get_current_user),
               reports_service: ReportsService = Depends(),
               ) -> dict[str, str]:
    """Import data from .csv file

    Args:
        file (UploadFile, optional): uploaded .csv file.
        Defaults to File(...).
        reports_service (ReportsService, optional): service to handle file.
        Defaults to Depends().

    Returns:
        dict[str, str]: waiting message
    """
    # Make import as background task
    background_tasks.add_task(reports_service.import_csv, user.id, file)
    # Or synchronously:
    # rows_statistics = reports_service.import_csv(user.id, file)->OperationsNumChange
    return {"message": "File for importing just has sent in the background"}
