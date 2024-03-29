from abc import ABC
from datetime import datetime, date
from typing import Optional, List

from pydantic.main import BaseModel

from formatters.bank_formatter import BankFormatter


class ConsolidatedRecord(BaseModel):
    date: date
    transaction: str
    deposit: Optional[float]
    withdrawal: Optional[float]
    bank: str

    @property
    def year_month(self):
        return f"{self.date.year}-{self.date.month:02d}"  # pad single-digit months with 0

    @property
    def output_date(self):
        return datetime.strftime(self.date, "%d %b %Y")


class TxtFormatter(BankFormatter, ABC):
    @classmethod
    def records_to_csv(cls, records: List[ConsolidatedRecord]):
        records.sort(key=lambda r: r.date)
        col_names = cls.get_consolidated_column_names()
        n_cols = len(col_names)
        output_rows = [col_names]
        for record in records:
            output_row = [None] * n_cols
            output_row[cls.__consolidated_columns__.DATE.value.col_num] = record.output_date
            output_row[cls.__consolidated_columns__.YEAR_MONTH.value.col_num] = record.year_month
            output_row[cls.__consolidated_columns__.TRANSACTION.value.col_num] = record.transaction
            output_row[cls.__consolidated_columns__.DEPOSIT.value.col_num] = record.deposit
            output_row[cls.__consolidated_columns__.WITHDRAWAL.value.col_num] = record.withdrawal
            output_row[cls.__consolidated_columns__.BANK.value.col_num] = record.bank
            output_rows.append(output_row)
        cls.write_to_csv(output_rows)
