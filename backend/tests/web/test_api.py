import json

import pytest

from core.repositories.people_counter import PeopleCounterRepository, SensorDoesNotExist


class TestWebhookAPI:

    def __get_repository(self):
        return PeopleCounterRepository()

    def __reset_test_db(self):
        repo = self.__get_repository()
        json.dump([], open(repo.dao.filepath, "w"))

    def create_and_assert_first(self, len_before, client, repository):
        with pytest.raises(SensorDoesNotExist):
            repository.get_by_name("abc")
        res = client.post(
            "/api/webhook",
            json={"name": "abc", "ts": "2018-11-14T13:34:49Z", "in": 3, "out": 2}
        )
        assert res.status_code == 201
        assert len_before + 1 == len(repository.all())
        assert repository.get_by_name("abc")

    def test_create_is_creating_if_not_already_exists(self, client):
        self.__reset_test_db()
        repo = self.__get_repository()
        len_before = repo.count()
        self.create_and_assert_first(len_before, client, repo)

    def test_create_2_times_just_update_and_not_create_duplicate(self, client):
        self.__reset_test_db()
        repo = self.__get_repository()
        len_before = repo.count()
        self.create_and_assert_first(len_before, client, repo)
        model = repo.get_by_name("abc")
        assert model.in_ == 3 and model.ts == "2018-11-14T13:34:49Z"
        res = client.post(
            "/api/webhook",
            json={"name": "abc", "ts": "2018-11-24T14:34:49Z", "in": 8, "out": 2}
        )
        assert len_before + 1 == len(repo.all())
        model = repo.get_by_name("abc")
        assert model.ts == "2018-11-24T14:34:49Z" and model.in_ == 8


class TestOccupancyAPI:
    def test_get_occupancy_for_specific_sensor(self, client):
        res = client.post(
            "/api/webhook",
            json={"name": "abc", "ts": "2018-11-14T13:34:49Z", "in": 3, "out": 2}
        )
        res = client.get(
            "/api/occupancy?sensor=abc"
        )
        assert res.status_code == 200 and res.json == {"inside": 1}

    def test_get_mean_occupancy(self, client):
        client.post(
            "/api/webhook",
            json={"name": "abc", "ts": "2018-11-14T13:34:49Z", "in": 5, "out": 2}
        )
        client.post(
            "/api/webhook",
            json={"name": "def", "ts": "2018-11-14T13:34:49Z", "in": 8, "out": 1}
        )
        res = client.get("/api/occupancy")
        assert res.status_code == 200
        assert res.json["mean_occupancy"] == 5
