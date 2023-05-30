from core.dao.in_memory import InMemoryDAO
from core.models.people_counter import PeopleCounter
from core.settings import USED_DAO_CLASS, DB_PATH


def get_dao():
    if isinstance(USED_DAO_CLASS, InMemoryDAO):
        return USED_DAO_CLASS()
    else:
        return USED_DAO_CLASS(DB_PATH)


class PeopleCounterRepository:
    """
    Repository that manages PeopleCounter model in interaction with a DAO plugged at runtime --> DIP
    """
    def __init__(self, dao=None):
        self.dao = dao or get_dao()
        self.model_cls = PeopleCounter

    def all(self):
        records = self.dao.list()
        if records:
            return [
                self.model_cls(**record) for record in records
            ]
        return []

    def get_by_name(self, name):
        return self.__get_by_unique(field="name", unique_value=name)

    def get_by_id(self, id_value):
        return self.__get_by_unique(field="id_", unique_value=id_value)

    def __get_by_unique(self, field, unique_value):
        try:
            return self.model_cls(
                **next(
                    self.dao.filter_by(field=field, value=unique_value)
                )
            )
        except StopIteration:
            raise SensorDoesNotExist(f"Sensor with {field} {unique_value} does not exists")

    def create(self, model):
        self.dao.add(model.__dict__)

    def update_or_create(self, model):
        """
        update or create record
        :param model: new model instance
        :return: Tuple[Bool, PeopleCounter]
        """
        try:
            element = self.get_by_name(model.name)
            self.dao.update(element.__dict__, model.__dict__)
            return False, model
        except SensorDoesNotExist:
            self.create(model)
            return True, model

    def get_mean_occupancy(self):
        all_models = self.all()
        return sum(map(lambda model: model.flow, all_models)) / len(all_models)

    def count(self, records=None):
        records = records or self.all()
        return len(records)


class SensorDoesNotExist(ValueError):
    pass
