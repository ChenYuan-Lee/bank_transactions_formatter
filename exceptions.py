from enum import Enum
from typing import Set


class UnexpectedHeaderRow(Exception):

    def __init__(self, missing_enums: Set[Enum]):
        msg = f"The following expected enums are missing in the header row: {missing_enums}."
        super().__init__(self, msg)
