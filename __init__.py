# coding: utf-8

import gauges


def gauge_factory(datastore):
    def get_gauge_handle(name, gauge_type='daily'):
        if gauge_type == 'daily':
            return gauges.DailyGauge(name, datastore)
        elif gauge_type == 'hourly':
            return gauges.HourlyGauge(name, datastore)
        else:
            raise Exception('Unknown gauge type %s' % gauge_type)
    return get_gauge_handle
