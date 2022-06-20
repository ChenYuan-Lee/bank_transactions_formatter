from enum import Enum
from typing import List

from data_models import Header
from formatters.csv_formatter import CSVFormatter


class POSBColumns(Enum):
    DATE = Header(name="Transaction Date", col_num=0)
    BANK_REFERENCE_CODE = Header(name="Reference", col_num=1)
    DEBIT = Header(name="Debit Amount", col_num=2)
    CREDIT = Header(name="Credit Amount", col_num=3)
    TRANSACTION_REF_1 = Header(name="Transaction Ref1", col_num=4)
    TRANSACTION_REF_2 = Header(name="Transaction Ref2", col_num=5)
    TRANSACTION_REF_3 = Header(name="Transaction Ref3", col_num=6)


class POSBFormatter(CSVFormatter):
    __bank_specific_columns__ = POSBColumns
    __bank_name__ = "POSB"

    FILE_NAME = "posb.csv"
    HEADER_ROW_NUM = 17
    INPUT_DATE_FORMAT = "%d %b %Y"

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        transaction_references = row[
            cls.__bank_specific_columns__.TRANSACTION_REF_1.value.col_num:
            cls.__bank_specific_columns__.TRANSACTION_REF_3.value.col_num + 1
        ]
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            cls.format_transaction_references(transaction_references)

        output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = \
            row[cls.__bank_specific_columns__.CREDIT.value.col_num].strip()

        output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = \
            row[cls.__bank_specific_columns__.DEBIT.value.col_num].strip()

    @classmethod
    def format_transaction_references(cls, transaction_references: List[str]) -> str:
        return " | ".join(transaction_references).strip()
