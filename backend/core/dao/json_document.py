import json
from json import JSONDecodeError

from core.dao.base import BaseDAOMixin


class JsonDocumentDAO(BaseDAOMixin):
    """
    Json Document Data Access Object layer implements BaseDAO "Interface"
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def __get_records(self):
        try:
            return json.load(open(self.filepath, "rb"))
        except JSONDecodeError as exc:
            print(exc)
            return []

    def list(self):
        return self.__get_records()

    def __write(self, records):
        json.dump(records, open(self.filepath, "w"))

    def add(self, record):
        records = self.__get_records()
        records.append(record)
        self.__write(records)
        return self

    def filter_by(self, field, value):
        return filter(
            lambda el: el[field] == value,
            self.__get_records()
        )

    def update(self, record, new_data):
        records = self.__get_records()
        idx = records.index(record)
        record = records[idx]
        record.update(new_data)
        records[idx] = record
        self.__write(records)


