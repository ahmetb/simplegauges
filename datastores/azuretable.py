# coding: utf-8

from datastore import *
from azure.storage import TableService

class AzureGaugeDatastore(GaugeDatastore):
    """Stores gauge data in Azure Table storage. Utilizes table storage 
    as follows:
    
    PartitionKey: gauge name
    RowKey: date key (e.g. day string)
    data: stored data for date key
    Timestamp: last time data updated

    Replaces existing rows (PK+RK) with upsert queries.
    """

    table_service = None
    table_name    = None

    def __init__(self, account_name, account_key, table_name):
        self.table_name = table_name
        self.table_service = TableService(account_name, account_key)

    def save_data(self, gauge_name, date_key, data):
        """Saves data to the row (replaces if exists)
        """

        entity = {'PartitionKey': gauge_name, 'RowKey': date_key, 'data': data}
        self.table_service.insert_or_replace_entity(self.table_name,
            gauge_name, date_key, entity)

    def get_gauge_data(self, gauge_name):
        """Retrieves all gauge data, returns unsorted
        """

        query = "PartitionKey eq '{0}'".format(gauge_name)
        rows = self.table_service.query_entities(self.table_name, filter=query)
        if rows:
            return [make_record(record.RowKey, record.data) for record in rows]

    def get_data(self, gauge_name, date_key):
        """Retrieves gauge data for a specific date key (e.g. day)
        """

        rec = self.table_service.get_entity(self.table_name, gauge_name, 
                                            date_key)
        if not rec:
            return None
        return make_record(rec.RowKey, rec.data)