# coding: utf-8

from dateutil import parser

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


    def save(self, day, value = 0):        
        daystr = str(day)
        self.datastore.save_data(self.name, daystr, value)


    def get(self, day):
        """None if data does not exist
        """

        daystr = str(day)
        record = self.datastore.get_data(self.name, daystr)
        if record:
            return self.make_daily_record(record)

    def __get_all(self):
        records = self.datastore.get_gauge_data(self.name)
        if records:
            return [self.make_daily_record(r) for r in records]


    def aggregate(self, data_points, aggregator = None, post_processor = None):
        data = self.__get_all()

        if not data:
            return []

        if aggregator:
            data = aggregator(data)

        if post_processor:
            data = post_processor(data)

        return data[-data_points:]


    @staticmethod
    def make_daily_record(record):
        """None if data does not exist
        """
        day = parser.parse(record['key']).date()
        return {'key': day, 'data': record['data']}
