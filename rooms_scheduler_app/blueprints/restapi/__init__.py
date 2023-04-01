from flask import Blueprint
from flask_restful import Api

from .room_resources import RoomsResource, RoomResource
from .schedule_resources import SchedulesResource, ScheduleResource, AccessRequestHandlerResource
from .user_resources import UsersResource, UserResource


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)

# Register api routes
api.add_resource(UsersResource, "/users/")
api.add_resource(UserResource, "/users/<int:user_id>")

api.add_resource(RoomsResource, "/rooms/")
api.add_resource(RoomResource, "/rooms/<int:room_id>")

api.add_resource(SchedulesResource, "/schedules/")
api.add_resource(ScheduleResource, "/schedules/<int:schedule_id>")

api.add_resource(AccessRequestHandlerResource, "/handler/access_request/<int:user_id>/<int:room_id>")

def init_app(app):
    app.register_blueprint(bp)
