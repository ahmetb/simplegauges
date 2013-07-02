# coding: utf-8

from datetime import timedelta
from helpers import make_record


def day_fill(data, fill_value=None):
    """Given a data set with missing day values sorted by day, adds records
    with value of `fill_value`
    """
    return generic_date_fill(1, data, fill_value)


def week_fill(data, fill_value=None):
    """Given a sorted data set with missing week keys, adds records with
    value of `fill_value`
    """
    return generic_date_fill(7, data, fill_value)


def generic_date_fill(day_interval, data, fill_value=None):
    new_data = list()
    prev = None
    for dt in data:
        if prev:
            diff = (dt['key'] - prev['key']).days / day_interval
            if diff > 1:
                for i in range(1, diff):
                    new_date = prev['key'] + timedelta(days=i*day_interval)
                    new_data.append(make_record(new_date, fill_value))
        new_data.append(dt)
        prev = dt
    return new_data
