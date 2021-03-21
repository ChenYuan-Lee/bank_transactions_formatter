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
        with open(cls.get_input_file_path()) as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')

            if cls.HAS_HEADER_ROW:
                for _ in range(cls.HEADER_ROW_NUM):
                    next(csv_reader)  # skip rows prior to the header row
                header_row = next(csv_reader)
                cls.validate_header_row(header_row)

            output_list = []
            for row in csv_reader:
                if not row:
                    continue  # skip empty rows

                output_row = cls.format_single_row(row)
                output_list.append(output_row)
            cls.sort_by_date(output_list)
            output_list = [cls.get_consolidated_column_names()] + output_list

        with open(cls.get_output_file_path(), mode='w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')
            for row in output_list:
                csv_writer.writerow(row)

        print(f"Successfully formatted `{cls.get_input_file_path()}` and saved to `{cls.get_output_file_path()}`.")

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
    def format_single_row(cls, row: List[str]):
        raise NotImplementedError

    @classmethod
    def convert_date_to_year_month(cls, date: datetime) -> str:
        return f"{date.year}-{date.month:02d}"  # pad single-digit months with 0

    @classmethod
    def sort_by_date(cls, output_list: list) -> None:
        output_list.sort(key=lambda output_row: output_row[cls.__consolidated_columns__.DATE.value.col_num])
        for row in output_list:
            row[cls.__consolidated_columns__.DATE.value.col_num] = \
                datetime.strftime(row[cls.__consolidated_columns__.DATE.value.col_num], cls.OUTPUT_DATE_FORMAT)

# create an enum class which maps to a ConsolidatedColumn object (which contains column num, and name)
# pass this enum as a class attribute, which can be accessed by the child classes
# the same enum class concept can be applied to the child class (e.g. DBSColumn object)

