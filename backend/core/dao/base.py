class BaseDAOMixin:
    def list(self):
        raise NotImplementedError("")

    def add(self, record):
        raise NotImplementedError("")

    def filter_by(self, field, value):
        raise NotImplementedError("")

    def update(self, record, new_data):
        raise NotImplementedError("")

