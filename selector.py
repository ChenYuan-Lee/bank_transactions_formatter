import os
from typing import List

from file_dt_checker import FileDTChecker
from formatters.bank_formatter import BankFormatter


class Selector:
    @classmethod
    def transform(cls, formatters: List[BankFormatter]) -> List[BankFormatter]:
        existing_files = []
        selected_formatters = []
        for formatter in formatters:
            fp = formatter.get_input_file_path()
            if os.path.isfile(fp):
                existing_files.append(fp)
                selected_formatters.append(formatter)
            else:
                print(f'`{fp}` not found, skipping.')
        FileDTChecker.transform(existing_files)
        return selected_formatters
