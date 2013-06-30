# coding: utf-8

from dateutil import parser
from helpers import make_record

class BaseGauge(object):
    pass


class DailyGauge(BaseGauge):
    """Stores one numeric record for per day.

    Return format:
        {'key':datetime.date, 'data':numeric}
    """

    def __init__(self, name, datastore):
        self.name = name
        self.datastore = datastore

    def save(self, day, value=0):
        daystr = str(day)
        self.datastore.save_data(self.name, daystr, value)

    def get(self, day):
        """None if data does not exist
        """

        daystr = str(day)
        record = self.datastore.get_data(self.name, daystr)
        if record:
            return self.make_daily_record(record)

    def __get_data(self, since_day, before_day=None):

        lower_limit_day = str(since_day)
        upper_limit_day = str(before_day) if before_day else before_day
        records = self.datastore.get_gauge_data(self.name, lower_limit_day,
                                                upper_limit_day)
        if records:
            return [self.make_daily_record(r) for r in records]

    def aggregate(self, data_since_day, data_before_day=None, aggregator=None,
                  take_last=0, post_processors=[]):
        data = self.__get_data(data_since_day, data_before_day)

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

    @staticmethod
    def make_daily_record(record):
        """None if data does not exist
        """

        day = parser.parse(record['key']).date()
        return make_record(day, record['data'])
