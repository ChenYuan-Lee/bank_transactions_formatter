import os
import shutil
from datetime import datetime, timedelta

from exceptions import LargeDTDelta

OUTPUT_DIR = 'output_files'
CONSOLIDATED_FP = 'consolidated.csv'
DT_DELTA_THRESHOLD = timedelta(days=1)


class Consolidator:
    earliest_dt = datetime.max
    earliest_fp = None
    latest_dt = datetime.min
    latest_fp = None

    @classmethod
    def transform(cls):
        with open(CONSOLIDATED_FP, 'w') as consolidated_file:
            for output_file in os.listdir(OUTPUT_DIR):
                output_fp = os.path.join(OUTPUT_DIR, output_file)
                cls.process_file_datetime(output_fp)
                with open(output_fp) as f:
                    next(f)  # remove repeated header
                    shutil.copyfileobj(f, consolidated_file)
        cls.raise_large_datetime_delta()

    @classmethod
    def process_file_datetime(cls, filepath: str):
        dt = datetime.fromtimestamp(os.path.getmtime(filepath))
        if dt < cls.earliest_dt:
            cls.earliest_dt = dt
            cls.earliest_fp = filepath
        if dt > cls.latest_dt:
            cls.latest_dt = dt
            cls.latest_fp = filepath

    @classmethod
    def raise_large_datetime_delta(cls):
        if cls.latest_dt - cls.earliest_dt >= DT_DELTA_THRESHOLD:
            raise LargeDTDelta(
                earliest_dt=cls.earliest_dt,
                earliest_fp=cls.earliest_fp,
                latest_dt=cls.latest_dt,
                latest_fp=cls.latest_fp,
            )
