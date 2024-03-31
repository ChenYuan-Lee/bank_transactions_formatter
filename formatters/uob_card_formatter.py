from datetime import datetime

from formatters.bank_formatter import BankFormatter, ConsolidatedRecord


class UobCardFormatter(BankFormatter):
    __bank_name__ = "UOB Credit Card"

    FILE_NAME = "uob_card.txt"

    @classmethod
    def transform(cls):
        with open(cls.get_input_file_path()) as f:
            lines = f.readlines()

        lines = [line.strip() for line in lines]
        records = []
        i = 0
        while i < len(lines):
            if lines[i][-3:] == ' CR':
                record = cls.build_record_for_credit(lines[i])
                i += 1
            else:
                record = cls.build_record_for_debit(*lines[i:i+2])
                i += 2

            records.append(record)

        cls.consolidated_records_to_csv(records)

    @classmethod
    def build_record_for_credit(cls, line: str):
        """
        Example record:
            25 Mar 2024	24 Mar 2024	PAYMT THRU E-BANK/HOMEB/CYBERB (EP21)	0.01 SGD CR
        """
        description = line.split('\t')[2]
        credit_amount, currency, _ = line.split('\t')[-1].split(' ')
        assert currency == 'SGD'

        return ConsolidatedRecord(
            date=cls.get_transact_date(line),
            transaction=description,
            deposit=credit_amount,
            bank=cls.__bank_name__,
        )

    @classmethod
    def build_record_for_debit(cls, line_1: str, line_2: str):
        """
        Example record:
            11 Mar 2024	06 Mar 2024	BUS/MRT 401805552 SINGAPORE SG
            Ref No: 74541834069288086020296	2.18 SGD
        """
        description = line_1.split('\t')[2]
        spent_amount, currency = line_2.split('\t')[-1].split(' ')
        assert currency == 'SGD'

        return ConsolidatedRecord(
            date=cls.get_transact_date(line_1),
            transaction=description,
            withdrawal=spent_amount,
            bank=cls.__bank_name__,
        )

    @classmethod
    def get_transact_date(cls, line: str):
        return datetime.strptime(line.split('\t')[1], "%d %b %Y").date()
