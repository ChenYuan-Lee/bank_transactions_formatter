from datetime import datetime
from enum import Enum
from typing import Set


class UnexpectedHeaderRow(Exception):

    def __init__(self, missing_enums: Set[Enum]):
        msg = f"The following expected enums are missing in the header row: {missing_enums}."
        super().__init__(self, msg)


class LargeDTDelta(Exception):
    def __init__(
        self,
        earliest_dt: datetime,
        earliest_fp: str,
        latest_dt: datetime,
        latest_fp: str,
    ):
        msg = f'Large difference detected between the last modified datetime of `{earliest_fp}` ({earliest_dt}) and ' \
              f'that of `{latest_fp}` ({latest_dt}) - delta of {(latest_dt - earliest_dt).days} days'
        super().__init__(self, msg)
