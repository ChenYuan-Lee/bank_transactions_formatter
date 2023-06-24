import shutil
from datetime import datetime
from typing import List

from file_dt_checker import FileDTChecker
from formatters.bank_formatter import BankFormatter

CONSOLIDATED_FP = 'consolidated.csv'


class Consolidator:
    earliest_dt = datetime.max
    earliest_fp = None
    latest_dt = datetime.min
    latest_fp = None

    @classmethod
    def transform(cls, formatters: List[BankFormatter]):
        output_filepaths = []
        for formatter in formatters:
            output_filepaths.append(formatter.get_output_file_path())
        FileDTChecker.transform(output_filepaths)
        with open(CONSOLIDATED_FP, 'w') as consolidated_file:
            for output_fp in output_filepaths:
                with open(output_fp) as f:
                    next(f)  # remove repeated header
                    shutil.copyfileobj(f, consolidated_file)
