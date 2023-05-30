import pytest

from core.dao.in_memory import InMemoryDAO
from core.repositories.people_counter import PeopleCounterRepository, SensorDoesNotExist


class TestPeopleCounterRepository:
    def __get_repository_to_test(self, records=None):
        records = records or [
            {"id_": 1, "ts": "2022-06-22T10:50", "name": "sensor xyz", "in_": 5, "out": 3},
            {"id_": 2, "ts": "2022-06-22T10:51", "name": "sensor abc", "in_": 2, "out": 1}
        ]
        return PeopleCounterRepository(
            InMemoryDAO(records)
        )

    def test_get_all_return_all(self):
        repo = self.__get_repository_to_test()
        all_record = repo.all()
        assert all(
            isinstance(el, repo.model_cls) for el in all_record
        )
        first_instance = all_record[0]
        assert first_instance.id_ == 1 and first_instance.name == "sensor xyz"

    def test_get_by_id_return_model_record(self):
        repo = self.__get_repository_to_test()
        instance = repo.get_by_id(1)
        assert instance.id_ == 1 and instance.name == "sensor xyz"
        instance = repo.get_by_id(2)
        assert instance.id_ == 2 and instance.name == "sensor abc"

    def test_get_unknown_id_raise_does_not_exist_exception(self):
        repo = self.__get_repository_to_test()
        with pytest.raises(SensorDoesNotExist):
            repo.get_by_id(555)

    def test_add_is_adding_to_records(self):
        repo = self.__get_repository_to_test()
        len_before = len(repo.all())
        model = repo.model_cls(
            name="sensor", ts="2022-06-22", in_=5, out=2
        )
        repo.create(model)
        assert len_before + 1 == len(repo.all())
        assert repo.get_by_id(model.id_)
