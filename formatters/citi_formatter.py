from enum import Enum
from typing import List

from data_models import Header
from formatters.bank_formatter import BankFormatter


class CitiColumns(Enum):
    DATE = Header(col_num=0)
    TRANSACTION = Header(col_num=1)
    WITHDRAWAL = Header(col_num=2)


class CitiFormatter(BankFormatter):
    __bank_specific_columns__ = CitiColumns
    __bank_name__ = "Citi"

    FILE_NAME = "citi.csv"
    HAS_HEADER_ROW = False
    INPUT_DATE_FORMAT = "%d/%m/%Y"

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            row[cls.__bank_specific_columns__.TRANSACTION.value.col_num]

        output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = cls.get_abs_value(
            row[cls.__bank_specific_columns__.WITHDRAWAL.value.col_num]
        )
