# coding: utf-8

import gauges
from datastores import azuretable


def daily_gauge_factory(datastore):
    def get_gauge_handle(name):
        return gauges.DailyGauge(name, datastore)
    return get_gauge_handle
