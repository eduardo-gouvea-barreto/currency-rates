"""
Functions to support date management.
"""

import datetime
from typing import List


def build_workdays_list(date_start: datetime.date, date_end: datetime.date) -> List[datetime.date]:
    """
    Constructs a list of workdays given a range of datas.
    """
    workdays_list = []
    date = date_start

    while date <= date_end:
        if is_workday(date):
            workdays_list.append(date)
        date += datetime.timedelta(days=1)

    return workdays_list


def is_workday(date: datetime.date) -> bool:
    """
    Predicate Function that checks if a date is a workday.
    """
    return date.weekday() not in [5, 6]
