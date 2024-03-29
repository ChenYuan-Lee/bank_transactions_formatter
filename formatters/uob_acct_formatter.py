import re
from datetime import datetime
from typing import List

from formatters.txt_formatter import ConsolidatedRecord, TxtFormatter


class UobAcctFormatter(TxtFormatter):
    __bank_name__ = "UOB Account"

    FILE_NAME = "uob_acct.txt"
    DATE_REGEX = r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}\b'

    @classmethod
    def transform(cls):
        with open(cls.get_input_file_path()) as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]
        records = []
        start = 0  # the first row contains the date of the first record
        i = 1  # begin scanning from the second row
        while i < len(lines):
            matches = re.findall(cls.DATE_REGEX, lines[i])
            if matches:
                record = cls.build_record(lines[start:i])
                records.append(record)
                start = i  # update start for next record

            i += 1

        final_record = cls.build_record(lines[start:i])
        records.append(final_record)
        cls.records_to_csv(records)

    @classmethod
    def build_record(cls, lines: List[str]):
        def format_money(money_str: str) -> float:
            assert money_str[-3:] == 'SGD'
            return float(money_str[:-3].replace(',', ''))

        withdrawal = lines[-3]
        deposit = lines[-2]
        if withdrawal == '-':
            withdrawal = None
            deposit = format_money(deposit)
        elif deposit == '-':
            withdrawal = format_money(withdrawal)
            deposit = None
        else:
            raise ValueError('Neither `deposit` nor `withdrawal` is `-`')

        date = datetime.strptime(lines[0], "%d %b %Y")
        description = '; '.join(lines[1:-3])

        return ConsolidatedRecord(
            date=date,
            transaction=description,
            deposit=deposit,
            withdrawal=withdrawal,
            bank=cls.__bank_name__,
        )
