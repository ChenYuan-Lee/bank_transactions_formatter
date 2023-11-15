import locale
from enum import Enum
from typing import List

from data_models import Header
from formatters.csv_formatter import CSVFormatter


class HSBCColumns(Enum):
    DATE = Header(col_num=0)
    DESCRIPTION = Header(col_num=1)
    DEPOSIT_OR_WITHDRAWAL = Header(col_num=2)


class HSBCFormatter(CSVFormatter):
    __bank_specific_columns__ = HSBCColumns
    __bank_name__ = "HSBC"

    FILE_NAME = "hsbc.csv"
    HAS_HEADER_ROW = False
    INPUT_DATE_FORMAT = "%d/%m/%Y"

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            row[cls.__bank_specific_columns__.DESCRIPTION.value.col_num]

        deposit_or_withdrawal: str = row[cls.__bank_specific_columns__.DEPOSIT_OR_WITHDRAWAL.value.col_num]
        deposit_or_withdrawal: float = locale.atof(deposit_or_withdrawal)
        if cls.is_positive_value(deposit_or_withdrawal):
            output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = \
                cls.get_abs_value(deposit_or_withdrawal)
        else:
            output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = \
                cls.get_abs_value(deposit_or_withdrawal)
