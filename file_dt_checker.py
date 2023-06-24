import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from exceptions import LargeDTDelta


class FileDTChecker:
    earliest_dt = datetime.max
    latest_dt = datetime.min
    earliest_fp = None
    latest_fp = None

    @classmethod
    def transform(
        cls,
        filepaths: List[Path],
        dt_delta_threshold: timedelta = timedelta(days=1),
    ):
        for filepath in filepaths:
            dt = datetime.fromtimestamp(os.path.getmtime(filepath))
            if dt < cls.earliest_dt:
                cls.earliest_dt = dt
                cls.earliest_fp = filepath
            if dt > cls.latest_dt:
                cls.latest_dt = dt
                cls.latest_fp = filepath
        cls.raise_large_datetime_delta(dt_delta_threshold)

    @classmethod
    def raise_large_datetime_delta(cls, dt_delta_threshold: timedelta):
        if cls.latest_dt - cls.earliest_dt >= dt_delta_threshold:
            raise LargeDTDelta(
                earliest_dt=cls.earliest_dt,
                earliest_fp=cls.earliest_fp,
                latest_dt=cls.latest_dt,
                latest_fp=cls.latest_fp,
            )
