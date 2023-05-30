from flask import Flask
from flask_cors import CORS

from web.api.people_counter import PeopleCounterWebhookAPIView, MeetingRoomOccupancyAPIView


def create_app():
    app = Flask(__name__)
    app.add_url_rule(
        "/api/webhook", view_func=PeopleCounterWebhookAPIView.as_view("api-webhook"), methods=["POST", "GET"]
    )
    app.add_url_rule(
        "/api/occupancy", view_func=MeetingRoomOccupancyAPIView.as_view("api-occupancy"), methods=["GET"]
    )
    CORS(app, resources=r'/api/*', allow_headers="*")
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
