import re
from enum import Enum
from typing import List, Union, Tuple

from data_models import Header
from formatters.bank_formatter import BankFormatter


class CitiStatementColumns(Enum):
    DATE = Header(col_num=0)
    TRANSACTION = Header(col_num=1)
    WITHDRAWAL_OR_DEPOSIT = Header(col_num=2)


class CitiStatementFormatter(BankFormatter):
    __bank_specific_columns__ = CitiStatementColumns
    __bank_name__ = "Citi"

    FILE_NAME = "citi_statement.txt"
    HAS_HEADER_ROW = False
    INPUT_DATE_FORMAT = "%d %b %Y"

    @classmethod
    def transform(cls):
        year = input("Input statement year (YYYY): ")
        with open(cls.get_input_file_path()) as f:
            lines = f.readlines()
        output_list = [cls.get_consolidated_column_names()]
        for line in lines:
            row = cls.prep_single_row(line=line, year=year)
            output_row = cls.format_single_row(row)
            output_list.append(output_row)
        cls.write_to_csv(output_list=output_list, output_file_path='output_files/citi_statement.csv')

    @classmethod
    def prep_single_row(
        cls,
        year: str,
        line: str,
    ) -> List[Union[str, re.Match]]:
        day_month_str = line[:6]  # e.g. "04 JUN"
        transaction_value_match = cls.get_transaction_value_match(line)
        transaction_desc = line[len(day_month_str) + 1:transaction_value_match.start()].strip()

        row = [None] * len(cls.__bank_specific_columns__)
        row[CitiStatementColumns.DATE.value.col_num] = f"{day_month_str} {year}"
        row[CitiStatementColumns.TRANSACTION.value.col_num] = transaction_desc
        row[CitiStatementColumns.WITHDRAWAL_OR_DEPOSIT.value.col_num] = transaction_value_match
        return row

    @classmethod
    def get_transaction_value_match(cls, line) -> re.Match:
        withdrawal_match = re.search("SG \d+\.\d{2}\n", line)  # e.g. "SG 5.28\n"
        deposit_match = re.search("\(\d+\.\d{2}\)\n", line)  # e.g. "(50.00)\n"
        transaction_value_match = withdrawal_match or deposit_match
        if transaction_value_match is None:
            raise ValueError(f"No transaction value found for: `{line}`")
        return transaction_value_match

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = \
            row[CitiStatementColumns.TRANSACTION.value.col_num]

        transaction_value_match = row[CitiStatementColumns.WITHDRAWAL_OR_DEPOSIT.value.col_num]
        is_deposit, transact_val = cls.format_transaction_value_match(transaction_value_match)

        if is_deposit:
            output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = transact_val
        else:
            output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = transact_val

    @classmethod
    def format_transaction_value_match(cls, transaction_value_match: re.Match) -> Tuple[bool, float]:
        transaction_value_str = transaction_value_match.group().strip() # strip to remove newline
        if transaction_value_str[0] == '(' and transaction_value_str[-1] == ')':  # e.g. "(50.00)"
            return True, float(transaction_value_str[1:-1])
        else:
            prefix = "SG "  # e.g. "SG 5.28"
            return False, float(transaction_value_str[len(prefix):])
