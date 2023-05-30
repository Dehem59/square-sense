from core.dao.base import BaseDAOMixin


class InMemoryDAO(BaseDAOMixin):
    """
    In Memory Data Access Object layer implements BaseDAO "Interface"
    """
    def __init__(self, records=None):
        self.records = records or []

    def list(self):
        return self.records

    def add(self, record):
        self.records.append(record)
        return self

    def filter_by(self, field, value):
        return filter(
            lambda el: el[field] == value, self.records
        )

    def update(self, record, new_data):
        idx = self.records.index(record)
        record.update(new_data)
        self.records[idx] = record


