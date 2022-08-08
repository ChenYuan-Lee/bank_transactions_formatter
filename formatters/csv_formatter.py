import csv
from typing import List

from formatters.bank_formatter import BankFormatter


class CSVFormatter(BankFormatter):
    FINAL_ROWS_TO_SKIP = NotImplemented
    STOPPING_ROW_NUM = NotImplemented

    @classmethod
    def transform(cls):
        if cls.FINAL_ROWS_TO_SKIP is not NotImplemented:
            cls.set_stopping_row_num()

        with open(cls.get_input_file_path(), mode='r', encoding='utf-8-sig') as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')

            if cls.HAS_HEADER_ROW:
                for _ in range(cls.HEADER_ROW_NUM):
                    next(csv_reader)  # skip rows prior to the header row
                header_row = next(csv_reader)
                cls.validate_header_row(header_row)

            output_list = []
            for i, row in enumerate(csv_reader):
                if cls.STOPPING_ROW_NUM is not NotImplemented:
                    row_num = (i + 1) + (cls.HEADER_ROW_NUM if cls.HEADER_ROW_NUM is not NotImplemented else 0)
                    if cls.STOPPING_ROW_NUM == row_num:
                        break

                # skip empty rows
                if not row:
                    continue

                # skip rows containing only tabs
                row = [value.strip('\t') for value in row]
                if all([value == '' for value in row]):
                    continue

                output_row = cls.format_single_row(row)
                output_list.append(output_row)

        cls.sort_by_and_format_date(output_list)
        output_list = [cls.get_consolidated_column_names()] + output_list

        cls.write_to_csv(output_list)

    @classmethod
    def set_stopping_row_num(cls) -> None:
        with open(cls.get_input_file_path(), mode='r', encoding='utf-8-sig') as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')
            row_count = sum(1 for _ in csv_reader)
            cls.STOPPING_ROW_NUM = row_count - cls.FINAL_ROWS_TO_SKIP

    @classmethod
    def custom_format_row(cls, row: List[str], output_row: list) -> None:
        raise NotImplementedError
