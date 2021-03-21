from enum import Enum
from typing import List

from data_models import Header
from formatters.bank_formatter import BankFormatter


class SCCardColumns(Enum):
    DATE = Header(name="Date", col_num=0)
    DESCRIPTION = Header(name="DESCRIPTION", col_num=1)
    FOREIGN_CURRENCY_AMT = Header(name="Foreign Currency Amount", col_num=2)
    SGD_AMT = Header(name="SGD Amount", col_num=3)


class SCCardFormatter(BankFormatter):
    __bank_specific_columns__ = SCCardColumns
    __bank_name__ = "SC_Card"

    FILE_NAME = "sc_card.csv"
    HEADER_ROW_NUM = 4
    INPUT_DATE_FORMAT = "%d/%m/%Y"
    FINAL_ROWS_TO_SKIP = 6

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            row[cls.__bank_specific_columns__.DESCRIPTION.value.col_num]

        cls.set_deposit_or_withdrawal(
            sgd_str=row[cls.__bank_specific_columns__.SGD_AMT.value.col_num],
            output_row=output_row,
        )

    @classmethod
    def set_deposit_or_withdrawal(cls, sgd_str: str, output_row: list) -> None:
        transact_type = sgd_str[-2:]  # either "DR" or "CR"
        sgd_value = sgd_str[3:-2].strip()  # remove "SGD" prefix, and "DR"/"CR" suffix
        if transact_type == "DR":
            output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = sgd_value
        elif transact_type == "CR":
            output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = sgd_value
        else:
            raise ValueError(f"Unexpected transaction type: `{transact_type}`.")
