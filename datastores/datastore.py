# coding: utf-8

class GaugeDatastore(object):
    def save_data(self, gauge_name, date_key, data):
        pass

    def get_gauge_data(self, gauge_name):
        """Retrieves all gauge data, returns sorted.

        Return format: [ {"key": date_key, "data": data}, ... ]
        For missing data, data field will be returned as None.

        """
        pass

    def get_data(self, gauge_name, date_key):
        """Retrieves gauge data for a specific date key (e.g. day)

        Return format: {"key": date_key, "data": data} 
        For missing data, data field will be returned as None.
        """
        pass

def make_record(date_key, data):
    return {'key': date_key, 'data': data }