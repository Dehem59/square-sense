from flask import request
from flask.views import MethodView
from flask_cors import cross_origin

from core.repositories.people_counter import PeopleCounterRepository
from web.serializers.people_counter import PeopleCounterSerializer


class BasePeopleRepositoryMixin:
    """
    Mixin to attach repository property can be inherited by Views
    """
    _repository = None

    @property
    def repository(self):
        if self._repository is None:
            self._repository = PeopleCounterRepository()
        return self._repository


class PeopleCounterWebhookAPIView(BasePeopleRepositoryMixin, MethodView):
    serializer = PeopleCounterSerializer

    def post(self):
        data = request.json
        model_instance = self.serializer.to_model(data)
        self.repository.update_or_create(model_instance)
        return {
            "detail": "information added"
        }, 201

    def get(self):
        return self.repository.dao.list()


class MeetingRoomOccupancyAPIView(BasePeopleRepositoryMixin, MethodView):

    def get(self):
        sensor = request.args.get("sensor")
        if not sensor:
            return {
                "detail": "No specific sensor provided",
                "mean_occupancy": self.repository.get_mean_occupancy()
            }
        model_instance = self.repository.get_by_name(sensor)
        return {"inside": model_instance.flow}



