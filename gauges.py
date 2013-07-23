# coding: utf-8

import datetime
from dateutil import parser
from helpers import make_record


class BaseGauge(object):
    pass


class BaseTimedGauge(BaseGauge):
    """Stores one numeric record for per specified

    Return format:
        {'key': datetime/date, 'data': numeric}
    """

    def __init__(self, name, datastore, date_converter, record_converter):
        """
        date_converter: function converts specified datetime to str by
            stripping out unnecessary parts
            e.g. converts passed datetime to date as str.

        record_converter: function takes object
            {'key': converted date as string, 'value': numeric} and replaces
            key with a parsed date/time value and returns a new object
        """
        self.name = name
        self.datastore = datastore

        if not callable(date_converter) or not callable(record_converter):
            raise Exception('Provided converter arguments are not callable')
        self.date_converter = date_converter
        self.record_converter = record_converter

    def save(self, date, value=0):
        """saves given value to specified date
        """

        datestr = self.date_converter(date)
        self.datastore.save_data(self.name, datestr, value)

    def get(self, date):
        """returns None if data does not exist
        """

        datestr = self.date_converter(date)
        record = self.datastore.get_data(self.name, datestr)
        if record:
            return self.record_converter(record)

    def __get_data(self, since_date, before_date=None):
        """retrieves sorted data set between two dates

        since_date: lower limit, inclusive
        before_date: optional. upper limit, exclusive
        """

        lower_limit_date = self.date_converter(since_date)
        upper_limit_date = self.date_converter(before_date) if before_date \
            else None
        records = self.datastore.get_gauge_data(self.name, lower_limit_date,
                                                upper_limit_date)
        if records:
            return [self.record_converter(r) for r in records]

    def aggregate(self, since_date, before_date=None, aggregator=None,
                  post_processors=[], take_last=0):
        """retrieves data within specified ranges and aggregates using given
        functions

        since_date: lower limit for data date, inclusive
        before_date: optional. upper limit for data date, exclusive
        aggregator: optional. aggregator function, takes record list and
            returns a new one after processing it
        post_processors: optional. list of functions takes a record list and
            returns new ones, used for post-processing aggregated data
        take_last: optional. picks last N records from result data and returns
        """

        data = self.__get_data(since_date, before_date)

        if take_last < 0:
            raise Exception('take_last argument cannot be negative')

        if not data:
            return []

        if aggregator:
            data = aggregator(data)

        if post_processors:
            for processor in post_processors:
                data = processor(data)

        return data[-take_last:]


class DailyGauge(BaseTimedGauge):
    """Stores one numeric record for per day.
    """

    def __init__(self, name, datastore):
        def day_converter(dt):
            """returns day of datetime as string"""
            if not isinstance(dt, datetime.datetime):
                raise Exception('DailyGauge takes only datetime type as time')

            day = dt.date()
            return str(day)

        def make_day_record(record):
            day = parser.parse(record['key']).date()
            return make_record(day, record['data'])

        BaseTimedGauge.__init__(self, name, datastore, day_converter,
                                make_day_record)


class HourlyGauge(BaseTimedGauge):
    """Stores one numeric record for per hour.
    """

    def __init__(self, name, datastore):
        def hour_converter(dt):
            """returns day+hour of datetime as string"""
            if not isinstance(dt, datetime.datetime):
                raise Exception('HourlyGauge takes only datetime type as time')
            hr = dt - datetime.timedelta(
                minutes=dt.minute,
                seconds=dt.second,
                microseconds=dt.microsecond)
            return str(hr)

        def make_timed_record(record):
            day = parser.parse(record['key'])
            return make_record(day, record['data'])

        BaseTimedGauge.__init__(self, name, datastore, hour_converter,
                                make_timed_record)
