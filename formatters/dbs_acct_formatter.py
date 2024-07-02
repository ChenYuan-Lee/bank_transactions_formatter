import csv
from datetime import datetime
from enum import Enum

from data_models import Header
from formatters.bank_formatter import ConsolidatedRecord
from formatters.csv_formatter import CSVFormatter


class DbsColumns(Enum):
    DATE = Header(name="Transaction Date", col_num=0)
    VALUE_DATE = Header(name="Value Date", col_num=1)
    STATEMENT_CODE = Header(name="Statement Code", col_num=2)
    REFERENCE = Header(name="Reference", col_num=3)
    DEBIT = Header(name="Debit Amount", col_num=4)
    CREDIT = Header(name="Credit Amount", col_num=5)
    CLIENT_REFERENCE = Header(name="Client Reference", col_num=6)
    ADDITIONAL_REFERENCE = Header(name="Additional Reference", col_num=7)
    MISC_REFERENCE = Header(name="Misc Reference", col_num=8)


class DbsAcctFormatter(CSVFormatter):
    __bank_specific_columns__ = DbsColumns
    __bank_name__ = "DBS Account"

    FILE_NAME = "dbs_acct.csv"
    HEADER_ROW_NUM = 19
    INPUT_DATE_FORMAT = "%d %b %Y"

    # TODO: remove this to rely on CSVFormatter's version upon refactoring of the latter
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

            records = []
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

                record = cls.build_record(row)
                records.append(record)

            cls.consolidated_records_to_csv(records)

    @classmethod
    def build_record(cls, row) -> ConsolidatedRecord:
        date = datetime.strptime(
            row[cls.__bank_specific_columns__.DATE.value.col_num],
            cls.INPUT_DATE_FORMAT
        ).date()
        transaction = ' | '.join([
            row[cls.__bank_specific_columns__.STATEMENT_CODE.value.col_num],
            row[cls.__bank_specific_columns__.REFERENCE.value.col_num],
            row[cls.__bank_specific_columns__.CLIENT_REFERENCE.value.col_num],
            row[cls.__bank_specific_columns__.ADDITIONAL_REFERENCE.value.col_num],
            row[cls.__bank_specific_columns__.MISC_REFERENCE.value.col_num],
        ])
        deposit = row[cls.__bank_specific_columns__.CREDIT.value.col_num]
        deposit = 0 if deposit == " " else deposit
        withdrawal = row[cls.__bank_specific_columns__.DEBIT.value.col_num]
        withdrawal = 0 if withdrawal == " " else withdrawal
        return ConsolidatedRecord(
            date=date,
            transaction=transaction,
            deposit=deposit,
            withdrawal=withdrawal,
            bank=cls.__bank_name__,
        )
