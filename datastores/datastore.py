# coding: utf-8


class GaugeDatastore(object):
    def save_data(self, gauge_name, date_key, data):
        """Saves specified data to date_key in specified gauge.
        date_key: str
        """
        pass

    def get_gauge_data(self, gauge_name, min_date_key=None, max_date_key=None):
        """Retrieves all gauge data, returns sorted.

        If min_date_key (str) is specified, returns records after specified
        date key (incl. min_date_key).

        If max_date_key (str) is specified, returns records before specified
        date key (excl. max_date_key).

        Return format: [ {"key": date_key, "data": data}, ... ]
        For missing data, data field will be returned as None.
        """
        pass

    def get_data(self, gauge_name, date_key):
        """Retrieves gauge data for a specific date key (e.g. day)

        date_key: str

        Return format: {"key": date_key, "data": data}
        For missing data, data field will be returned as None.
        """
        pass


def make_record(date_key, data):
    return {'key': date_key, 'data': data}
