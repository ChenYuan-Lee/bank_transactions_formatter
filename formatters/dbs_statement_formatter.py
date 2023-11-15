import locale
import os
from enum import Enum
from pathlib import Path
from typing import List

from data_models import Header
from formatters.bank_formatter import BankFormatter


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class DBSStatementColumns(Enum):
    DATE = Header(col_num=0)
    TRANSACTION = Header(col_num=1)
    WITHDRAWAL_OR_DEPOSIT = Header(col_num=2)


class DBSStatementFormatter(BankFormatter):
    __bank_specific_columns__ = DBSStatementColumns
    __bank_name__ = "DBS"

    FILE_NAME = "dbs_statement.txt"
    HAS_HEADER_ROW = False
    INPUT_DATE_FORMAT = "%d %b %Y"
    CURRENCY_PREFIX = 'S$'
    NUM_ROWS_PER_ITEM = 3

    @classmethod
    def transform(cls):
        with open(cls.get_input_file_path()) as f:
            lines = f.readlines()
        output_list = []
        for i in range(0, len(lines), cls.NUM_ROWS_PER_ITEM):
            row = cls.prep_single_row(*lines[i:i+cls.NUM_ROWS_PER_ITEM])
            output_row = cls.format_single_row(row)
            output_list.append(output_row)
        cls.sort_by_and_format_date(output_list)
        output_list = [cls.get_consolidated_column_names()] + output_list
        cls.write_to_csv(output_list=output_list)

    @classmethod
    def prep_single_row(cls, date_str: str, transaction_desc: str, amount_str: str):
        row = [None] * len(cls.__bank_specific_columns__)
        row[cls.__bank_specific_columns__.DATE.value.col_num] = date_str.strip()
        row[cls.__bank_specific_columns__.TRANSACTION.value.col_num] = transaction_desc.strip()
        row[cls.__bank_specific_columns__.WITHDRAWAL_OR_DEPOSIT.value.col_num] = amount_str.strip()
        return row

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            row[DBSStatementColumns.TRANSACTION.value.col_num]

        transact_amt: str = row[cls.__bank_specific_columns__.WITHDRAWAL_OR_DEPOSIT.value.col_num]
        transact_amt: str = transact_amt.strip(cls.CURRENCY_PREFIX)
        if transact_amt[-3:] == ' cr':
            output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = locale.atof(transact_amt[:-3])
        else:
            output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = locale.atof(transact_amt)

    @classmethod
    def get_output_file_path(cls) -> Path:
        filename, _ = os.path.splitext(super().get_output_file_path())
        return Path(filename + '.csv')
