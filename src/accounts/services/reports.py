# pylint: disable=missing-module-docstring
import csv
from io import StringIO
from typing import Any

from fastapi import Depends, HTTPException, status
from starlette.datastructures import UploadFile

from ..models.operations import Operation, OperationCreate, OperationsNumChange
from .operations import OperationsService

FILDNAMES = ['date', 'kind', 'amount', 'description']


class ReportsService:
    """Class to import and export .csv's"""
    def __init__(self, operations_service: OperationsService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: UploadFile) -> OperationsNumChange:
        """Import data from .csv to database

        Args:
            user_id (int): user id of operations owner
            file (UploadFile): file in bytes
        Returns:
            OperationsNumChange: number of rows
        """
        rows_number_before = self.operations_service.get_row_counts(user_id)

        if not file.filename.endswith(".csv"):
                raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)       
        reader = csv.DictReader(
            (line.decode() for line in file.file),
            fieldnames=FILDNAMES,
        )

        operations = []
        next(reader, None)  # skip the headers
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operations_service.create_many(user_id, operations,)

        rows_number_after = self.operations_service.get_row_counts(user_id)
        return OperationsNumChange(rows_number_before=rows_number_before,
                                   rows_number_after=rows_number_after)

    def export_csv(self, user_id: int) -> Any:
        """Export data of specific user to .csv

        Args:
            user_id (int): user id whoes data is required to download

        Returns:
            Any: .csv file
        """
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=FILDNAMES,
            extrasaction='ignore',  # no more fileds than in fildnames
        )

        operations = self.operations_service.get_list(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)  # to set cursor to the beginning
        return output
