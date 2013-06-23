# coding: utf-8

import gauges
from datastores import azuretable


default_datastore = None

def get_daily_gauge(name, datastore=None):
    return gauges.DailyGauge(name, datastore)
