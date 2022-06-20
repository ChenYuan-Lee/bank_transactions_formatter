from enum import Enum
from typing import List

from data_models import Header
from formatters.csv_formatter import CSVFormatter


class SCAcctColumns(Enum):
    DATE = Header(name="Date", col_num=0)
    TRANSACTION = Header(name="Transaction", col_num=1)
    CURRENCY = Header(name="Currency", col_num=2)
    DEPOSIT = Header(name="Deposit", col_num=3)
    WITHDRAWAL = Header(name="Withdrawal", col_num=4)
    RUNNING_BAL = Header(name="Running Balance", col_num=5)
    SGD_EQUIVALENT_BAL = Header(name="SGD Equivalent Balance", col_num=6)


class SCAcctFormatter(CSVFormatter):
    __bank_specific_columns__ = SCAcctColumns
    __bank_name__ = "SC_Acct"

    FILE_NAME = "sc_acct.csv"
    HEADER_ROW_NUM = 5
    INPUT_DATE_FORMAT = "%d/%m/%Y"

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            row[cls.__bank_specific_columns__.TRANSACTION.value.col_num]

        output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = \
            row[cls.__bank_specific_columns__.DEPOSIT.value.col_num]

        output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = \
            row[cls.__bank_specific_columns__.WITHDRAWAL.value.col_num]
