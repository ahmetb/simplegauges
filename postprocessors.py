# coding: utf-8

import datetime
from helpers import make_record


def day_fill(data, fill_value = None):
    """Given a data set with missing day values sorted by day, adds records
    with value of `fill_value`
    """
    
    new_data = list()
    prev = None
    for dt in data:
        if prev:
            day_diff = (dt['key'] - prev['key']).days
            if day_diff > 1:
                for i in range(1, day_diff):
                    new_date = prev['key'] + datetime.timedelta(days = i)
                    new_data.append(make_record(new_date, fill_value))
        new_data.append(dt)
        prev = dt
    return new_data