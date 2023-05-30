import uuid
from unittest.mock import patch

from core.models.people_counter import PeopleCounter


class TestPeopleCounterModel:
    @patch("core.models.people_counter.ID_GENERATOR", return_value="xyz")
    def test_instantiate_model_set_id(self, _):
        model = PeopleCounter(
            name="sensor", ts="2022-06-22", in_=5, out=2
        )
        assert model.id_ == "xyz"

    def test_model_get_flow(self):
        model = PeopleCounter(
            name="sensor", ts="2022-06-22", in_=5, out=2
        )
        assert model.flow == 3
        model.in_ = 10
        model.out = 4
        assert model.flow == 6

