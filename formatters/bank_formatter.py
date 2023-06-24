import csv
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List

from data_models import Header
from exceptions import UnexpectedHeaderRow

INPUT_FILES_DIRECTORY = "input_files"
OUTPUT_FILES_DIRECTORY = "output_files"


class ConsolidatedColumns(Enum):
    DATE = Header(name="Date", col_num=0)
    YEAR_MONTH = Header(name="Year-Month", col_num=1)
    TRANSACTION = Header(name="Transaction", col_num=2)
    CATEGORY = Header(name="Category", col_num=3)
    DEPOSIT = Header(name="Deposit", col_num=4)
    WITHDRAWAL = Header(name="Withdrawal", col_num=5)
    BANK = Header(name="Bank", col_num=6)


class BankFormatter:
    __consolidated_columns__ = ConsolidatedColumns
    __bank_specific_columns__ = NotImplemented
    __bank_name__ = NotImplemented

    FILE_NAME = NotImplemented
    HAS_HEADER_ROW = True
    HEADER_ROW_NUM = NotImplemented  # 0-based numbering
    INPUT_DATE_FORMAT = NotImplemented
    OUTPUT_DATE_FORMAT = "%d %b %Y"

    @classmethod
    def transform(cls):
        raise NotImplementedError

    @classmethod
    def get_input_file_path(cls) -> Path:
        return Path(INPUT_FILES_DIRECTORY, cls.FILE_NAME)

    @classmethod
    def get_output_file_path(cls) -> Path:
        return Path(OUTPUT_FILES_DIRECTORY, cls.FILE_NAME)

    @classmethod
    def get_consolidated_column_names(cls) -> List[str]:
        return [column.value.name for column in cls.__consolidated_columns__]

    @classmethod
    def validate_header_row(cls, header_row: List[str]) -> None:
        # Construct an enum set for the header row
        header_row_enums = set()
        for col_num, header_name in enumerate(header_row):
            header_name = header_name.strip('\t')
            header = Header(name=header_name, col_num=col_num)
            enum = cls.__bank_specific_columns__(header)
            header_row_enums.add(enum)

        # Compare the constructed enum set with the expected one. Any discrepancy can only mean a missing enum in the
        # constructed set that is present in the expected set, or an error would have been thrown above during
        # instantiation of __bank_specific_columns__.
        expected_enums = set(cls.__bank_specific_columns__.__members__.values())
        if header_row_enums != expected_enums:
            missing_enums = expected_enums - header_row_enums
            raise UnexpectedHeaderRow(missing_enums)

    @classmethod
    def format_single_row(cls, row: List[str]) -> list:
        output_row = [None] * len(cls.__consolidated_columns__)
        cls.format_date_cols(row, output_row)
        cls.insert_bank_name(output_row)
        cls.custom_format_row(row, output_row)
        return output_row

    @classmethod
    def format_date_cols(cls, row: List[str], output_row: list) -> None:
        date_str = row[cls.__bank_specific_columns__.DATE.value.col_num]
        date = datetime.strptime(date_str, cls.INPUT_DATE_FORMAT)
        output_row[cls.__consolidated_columns__.YEAR_MONTH.value.col_num] = \
            f"{date.year}-{date.month:02d}"  # pad single-digit months with 0

        output_row[cls.__consolidated_columns__.DATE.value.col_num] = date

    @classmethod
    def insert_bank_name(cls, output_row: list) -> None:
        output_row[cls.__consolidated_columns__.BANK.value.col_num] = cls.__bank_name__

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        raise NotImplementedError

    @classmethod
    def get_abs_value(cls, value: str) -> float:
        return abs(float(value))

    @classmethod
    def is_positive_value(cls, value: str) -> bool:
        return float(value) > 0

    @classmethod
    def sort_by_and_format_date(cls, output_list: list) -> None:
        output_list.sort(key=lambda output_row: output_row[cls.__consolidated_columns__.DATE.value.col_num])
        for output_row in output_list:
            output_row[cls.__consolidated_columns__.DATE.value.col_num] = \
                datetime.strftime(output_row[cls.__consolidated_columns__.DATE.value.col_num], cls.OUTPUT_DATE_FORMAT)

    @classmethod
    def write_to_csv(cls, output_list: List[list]):
        fp = cls.get_output_file_path()
        with open(fp, mode='w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')
            for row in output_list:
                csv_writer.writerow(row)
        print(f"Successfully saved to `{fp}`.")
