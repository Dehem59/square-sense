import json
from pathlib import Path

from core.dao.in_memory import InMemoryDAO
from core.dao.json_document import JsonDocumentDAO


class TestInMemoryDao:
    def test_in_memory_dao_can_list(self):
        dao = InMemoryDAO()
        dao.records = [
            {"id": 1, "name": "sensor xyz", "in": 2, "out": 1},
            {"id": 2, "name": "sensor abc", "in": 2, "out": 8},
        ]
        assert dao.list() == [
            {"id": 1, "name": "sensor xyz", "in": 2, "out": 1},
            {"id": 2, "name": "sensor abc", "in": 2, "out": 8},
        ]

    def test_dao_add_is_adding_record(self):
        dao = InMemoryDAO()
        assert dao.list() == []
        dao.add({"id": 1, "name": "super sensor"})
        assert dao.list() == [{"id": 1, "name": "super sensor"}]

    def test_filter_by_field_return_good_elements(self):
        dao = InMemoryDAO(records=[
            {"id": 1, "name": "sensor xyz", "in": 2, "out": 1},
            {"id": 2, "name": "sensor abc", "in": 2, "out": 8},
        ])
        assert list(dao.filter_by(field="id", value=1)) == [
            {"id": 1, "name": "sensor xyz", "in": 2, "out": 1},
        ]
        assert list(
            dao.filter_by(field="in", value=2)
        ) == dao.list()


class TestJsonDocumentDAO:

    def __get_dao(self):
        filepath = Path(__file__).parent / "data/fake_db.json"
        json.dump(
            [
                {
                    "id": 1,
                    "name": "sensor wyz",
                    "in": 4,
                    "out": 8
                },
                {
                    "id": 2,
                    "name": "sensor abc",
                    "in": 22,
                    "out": 10
                },
                {
                    "id": 3,
                    "name": "sensor quali",
                    "in": 4,
                    "out": 14
                }
            ],
                open(filepath, "w")
        )
        return JsonDocumentDAO(
            Path(__file__).parent / "data/fake_db.json"
        )

    def test_json_dao_can_list(self):
        dao = self.__get_dao()
        assert dao.list() == [
          {
            "id": 1, "name": "sensor wyz", "in": 4, "out": 8
          },
          {
            "id": 2, "name": "sensor abc", "in": 22, "out": 10
          },
          {
            "id": 3, "name": "sensor quali", "in": 4, "out": 14
          }
        ]

    def test_add_is_adding_record(self):
        dao = self.__get_dao()
        before = len(dao.list())
        dao.add(
            {"id": 4, "name": "my sensor", "in": 3, "out": 8}
        )
        list_after = dao.list()
        assert before + 1 == len(list_after)
        assert {"id": 4, "name": "my sensor", "in": 3, "out": 8} in list_after

    def test_dao_is_filtering(self):
        dao = self.__get_dao()
        assert list(dao.filter_by(field="in", value=4)) == [
            {
                "id": 1, "name": "sensor wyz", "in": 4, "out": 8
            },
            {
                "id": 3, "name": "sensor quali", "in": 4, "out": 14
            }
        ]
        assert list(dao.filter_by(field="id", value=2))[0] == {
            "id": 2, "name": "sensor abc", "in": 22, "out": 10
          }
